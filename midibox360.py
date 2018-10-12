#!/usr/bin/env python3

import toml
import mido
import pygame

default_config = """
# Choose which port midiBox360 outputs to. Must be inside quotation marks.
# An empty string can be used to choose the system's default port.
port = ""

# Select a mode to play in based on scale degree. Can be a number from 1 to 7.
# 1 = ionian (major); 2 = dorian; 3 = phrygyan; 4 = lydian; 5 = mixolydian;
# 6 = aeolian (minor); 7 = locrian
mode = 1

# Select a MIDI channel to output to. Can be a number from 1 to 16.
channel = 4

# Select a note to be used as the root note. Can be a number from 0 to 127.
# 60 = middle C
base_note = 60

[controls]
# Change which buttons the face buttons are mapped to.
# Valid values: "a", "b", "x", "y".
a_button = "a"
b_button = "b"
x_button = "x"
y_button = "y"
"""

# Find which note to play.
def msg(diastep, semitone):
    return mido.Message('note_on', channel=channel, note=(base_note + semitone\
                        + 12 * octave + notes[play + diastep + mode]) % 128)

# Map gamepad's face buttons
def buttonmap(button):
    if button == "a":
        button = 0
    if button == "b":
        button = 1
    if button == "x":
        button = 2
    if button == "y":
        button = 3
    return button

# Load configuration file if it exists. Otherwise generate default config file.
try:
    config_file = open('config.toml', 'r')
    config = toml.load(config_file)
except FileNotFoundError:
    config = toml.loads(default_config)
    with open('config.toml', 'w', encoding="utf-8") as f:
        f.write(default_config.lstrip())

# Init pygame and set it as mido's MIDI backend.
pygame.init()
pygame.joystick.init()
mido.set_backend('mido.backends.pygame')

# List of all numbers from 0 to 127 in a diatonic scale pattern.
notes = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28,29,31,33,35,
         36,38,40,41,43,45,47,48,50,52,53,55,57,59,60,62,64,65,67,69,71,
         72,74,76,77,79,81,83,84,86,88,89,91,93,95,96,98,100,101,103,105,107,
         108,110,112,113,115,117,119,120,122,124,125,127]

# Load values from config file.
mode = config['mode'] - 1
channel = config['channel'] - 1
base_note = config['base_note'] - notes[mode]
port = config['port']
a_btn = buttonmap(config['controls']['a_button'])
b_btn = buttonmap(config['controls']['b_button'])
x_btn = buttonmap(config['controls']['x_button'])
y_btn = buttonmap(config['controls']['y_button'])
octave = 0

# Open output port.
if port == '':
    outport = mido.open_output()
else:
    outport = mido.open_output(port)

# Show program window.
screen = pygame.display.set_mode([256, 128])
pygame.display.set_caption("midiBox360")

clock = pygame.time.Clock()

done = False

# Main program loop.
while done==False:
    joystick_count = pygame.joystick.get_count()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        # Move base note up or down an octave/semitone.
        if event.type == pygame.JOYHATMOTION:
                if joystick.get_hat(0) == (1,0):
                    base_note = (base_note + 1) % 128
                if joystick.get_hat(0) == (-1,0):
                    base_note = (base_note - 1) % 128
                if joystick.get_hat(0) == (0,1):
                    base_note = (base_note + 12) % 128
                if joystick.get_hat(0) == (0,-1):
                    base_note = (base_note - 12) % 128

        # Detect button presses.
        if event.type == pygame.JOYBUTTONDOWN:
            # Assign joystick events.
            root = joystick.get_button(a_btn) or joystick.get_button(b_btn)\
                   or joystick.get_button(x_btn)
            chord = joystick.get_button(b_btn) or joystick.get_button(x_btn)
            seventh = joystick.get_button(b_btn)
            set_mode = joystick.get_button(y_btn)
            chord_mode = joystick.get_axis(0) > 0.2 # left stick right
            maj_chord = joystick.get_button(y_btn)
            min_chord = joystick.get_button(a_btn)
            dom_chord = joystick.get_button(b_btn)
            dim_chord = joystick.get_button(x_btn)
            bumpers = joystick.get_button(4) or joystick.get_button(5)

            play = 0
            octave = 0
            # Define note to be played.
            if joystick.get_axis(2) > 0.8: # left trigger
                play += 1
            if joystick.get_button(4) == 1: # left bumper
                play += 2
            if joystick.get_button(5) == 1: # right bumper
                play += 4
            if joystick.get_axis(1) < -0.8: # left stick up
                octave = 1
            if joystick.get_axis(1) > 0.8: # left stick down
                octave = -1

            if not chord_mode:
                # Play diationic chords.
                if root:
                    outport.send(msg(0, 0))
                if chord:
                    outport.send(msg(2, 0))
                    outport.send(msg(4, 0))
                if seventh:
                    outport.send(msg(6, 0))
                if set_mode:
                    mode = play % 7
                    base_note = config['base_note'] - notes[mode]
            else:
                # Play specific chord quality.
                if maj_chord:
                    outport.send(msg(0,0))
                    outport.send(msg(0,4))
                    outport.send(msg(0,7))
                elif min_chord:
                    outport.send(msg(0,0))
                    outport.send(msg(0,3))
                    outport.send(msg(0,7))
                elif dom_chord:
                    outport.send(msg(0,0))
                    outport.send(msg(0,4))
                    outport.send(msg(0,7))
                    outport.send(msg(0,10))
                elif dim_chord:
                    outport.send(msg(0,0))
                    outport.send(msg(0,3))
                    outport.send(msg(0,6))
                    outport.send(msg(0,9))

        if event.type == pygame.JOYBUTTONUP:
            # Release all notes.
                for i in range(0, 127):
                    outport.send(mido.Message('note_off', channel=channel, note=i))

    clock.tick(0)

pygame.quit()
quit()
