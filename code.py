import board
import pulseio
import time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

def note(name):
  octave = int(name[-1])
  pitch = PITCHES.index(name[:-1].lower())
  return int(440 * 2 ** ((octave - 4) + (pitch - 9) / 12))

def get_voltage(pin):
  return (pin.value * 3.3) / 65536

# Switch variables
switch = DigitalInOut(board.D7)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

# Buzzer variables
PITCHES = "c,c#,d,d#,e,f,f#,g,g#,a,a#,b".split(",")
ON = 2 ** 15
OFF = 0

sequence = [
  ("d4", 8), ("d4", 8), ("e4", 4), ("d4", 4), ("g4", 4), ("f#4", 2), (None, 4),
  ("d4", 8), ("d4", 8), ("e4", 4), ("d4", 4), ("a4", 4), ("g4", 2), (None, 4),
  ("d4", 8), ("d4", 8), ("d5", 4), ("b4", 4), ("g4", 4), ("f#4", 4), ("e4", 4), (None, 4),
  ("c5", 8), ("c5", 8), ("b4", 4), ("g4", 4), ("a4", 4), ("g4", 2)
]

buzzer = pulseio.PWMOut(board.A1, frequency=500, duty_cycle=OFF, variable_frequency=True)

# candle variables
candle = DigitalInOut(board.D12)
candle.direction = Direction.OUTPUT

# Wait until the button is pressed
while switch.value:
  pass

# "Light" the "candle"
candle.value = True

# Play the music
for (notename, eigths) in sequence:
  buzzer.duty_cycle = OFF
  length = 2 / eigths
  if notename:
    buzzer.frequency = note(notename)
    buzzer.duty_cycle = ON
  time.sleep(length)

# Convert buzzer to a wind detector
buzzer.deinit()
blow = AnalogIn(board.A1)
time.sleep(0.2)

# Wait until someone blows on the buzzer, then blow out the candle!
while True:
  voltage = get_voltage(blow)
  if voltage > 2.5:
    candle.value = False
    break
  time.sleep(0.1)
