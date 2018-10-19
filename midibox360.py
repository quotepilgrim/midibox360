#!/usr/bin/env python3

import os
import sys
import platform
import toml
import mido
import mido.backends.pygame
import pygame

# Determine config file location.
if platform.system() == 'Windows':
    config_dir = os.environ['LOCALAPPDATA']
else:
    config_dir = os.path.join(os.environ['HOME'], '.config')

root = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(config_dir, 'midibox360')
config_file = os.path.join(config_dir, 'config.toml')
logo_path = ['/usr/share/midibox360/images',
             '/usr/local/share/midibox360/images',
             os.path.join(root, 'res')]
logo = 'logo.png'

for f in logo_path:
    f = os.path.join(f, logo)
    if os.path.isfile(f):
        logo = f

# Default config file contents.
default_config = """
# Choose which port midiBox360 outputs to. Must be inside quotation marks.
# An empty string can be used to choose the system's default port.
port = ""

# ID of joystick to be used.
joystick = 0

# Select a mode to play in based on scale degree. Can be a number from 1 to 7.
# 1 = ionian (major); 2 = dorian; 3 = phrygian; 4 = lydian; 5 = mixolydian;
# 6 = aeolian (minor); 7 = locrian
mode = 1

# Select a MIDI channel to output to. Can be a number from 1 to 16.
channel = 4

# Select a note to be used as the root note. Can be a number from 0 to 127.
# 60 = middle C
base_note = 60

[controls]
# Controller mapping. Buttons are numbers from 0 to 9;
# Axes are values from "axis_0" up to "axis_5" (with quotes).
a_button = 0
b_button = 1
x_button = 2
y_button = 3
left_bumper = 4
right_bumper = 5
back = 6
start = 7
left_thumb = 8
right_thumb = 9

# Triggers are axes on an Xbox 360 controller, but might be buttons otherwise.
# "right_trigger" is a special case on Windows; should be set to "axis_5"
# on Linux if using an Xbox 360 controller. Check README for more info.
left_trigger = "axis_2"
right_trigger = "axis_2"

left_stick_x = "axis_0"
left_stick_y = "axis_1"

right_stick_x = "axis_4"
right_stick_y = "axis_3"

dpad_up = "up"
dpad_down = "down"
dpad_left = "left"
dpad_right = "right"

# Invert axes. Values can be set to true or false.
axis_0_inv = false
axis_1_inv = false
axis_2_inv = false
axis_3_inv = false
axis_4_inv = false
axis_5_inv = false
"""

# Find which note to play.
def msg(diastep, semitone):
    return mido.Message('note_on', channel=channel, note=(base_note + semitone
                        + 12 * octave + notes[play + diastep + mode]) % 128)

# Get joystick event.
def get_event(event):
    if event == 'axis_0':
        event = joystick.get_axis(0) * axis_0_inv > 0.5
    elif event == 'axis_0_neg':
        event = joystick.get_axis(0) * axis_0_inv < -0.5
    elif event == 'axis_1':
        event = joystick.get_axis(1) * axis_1_inv > 0.5
    elif event == 'axis_1_neg':
        event = joystick.get_axis(1) * axis_1_inv < - 0.5
    elif event == 'axis_2':
        event = joystick.get_axis(2) * axis_2_inv > 0.5
    elif event == 'axis_2_neg':
        event = joystick.get_axis(2) * axis_2_inv < -0.5
    elif event == 'axis_3':
        event = joystick.get_axis(3) * axis_3_inv > 0.5
    elif event == 'axis_3_neg':
        event = joystick.get_axis(3) * axis_3_inv < - 0.5
    elif event == 'axis_4':
        event = joystick.get_axis(4) * axis_4_inv > 0.5
    elif event == 'axis_4_neg':
        event = joystick.get_axis(4) * axis_4_inv < - 0.5
    elif event == 'axis_5':
        event = joystick.get_axis(5) * axis_5_inv > 0.5
    elif event == 'axis_5_neg':
        event = joystick.get_axis(5) * axis_5_inv < - 0.5
    elif event == 'up':
        event = joystick.get_hat(0) == (0,1)
    elif event == 'down':
        event = joystick.get_hat(0) == (0,-1)
    elif event == 'left':
        event = joystick.get_hat(0) == (-1,0)
    elif event == 'right':
        event = joystick.get_hat(0) == (1,0)
    else:
        event = joystick.get_button(event)
    return event

# Load configuration file if it exists. Otherwise generate default config file.
if os.path.isfile(config_file):
    config = toml.load(config_file)
else:
    config = toml.loads(default_config)
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    with open(config_file, 'w', encoding="utf-8") as f:
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
octave = 0
playing = 0

# Load values from config file.
controls = config['controls']
joystick_id = config['joystick']
mode = config['mode'] - 1
channel = config['channel'] - 1
base_note = config['base_note'] - notes[mode]
port = config['port']

a_button = controls['a_button']
b_button = controls['b_button']
x_button = controls['x_button']
y_button = controls['y_button']
l_bumper = controls['left_bumper']
r_bumper = controls['right_bumper']
back = controls['back']
start = controls['start']
l_thumb = controls['left_thumb']
r_thumb = controls['right_thumb']

l_trigger = controls['left_trigger']
r_trigger = controls['right_trigger']
if r_trigger == l_trigger:
    r_trigger += '_neg'

l_stick_up = controls['left_stick_y'] + '_neg'
l_stick_down = controls['left_stick_y']
l_stick_left = controls['left_stick_x'] + '_neg'
l_stick_right = controls['left_stick_x']

r_stick_up = controls['right_stick_y'] + '_neg'
r_stick_down = controls['right_stick_y']
r_stick_left = controls['right_stick_x'] + '_neg'
r_stick_right = controls['right_stick_x']

hat_up = controls['dpad_up']
hat_down = controls['dpad_down']
hat_left = controls['dpad_left']
hat_right = controls['dpad_right']

axis_0_inv = -1 if controls['axis_0_inv'] else 1
axis_1_inv = -1 if controls['axis_1_inv'] else 1
axis_2_inv = -1 if controls['axis_2_inv'] else 1
axis_3_inv = -1 if controls['axis_3_inv'] else 1
axis_4_inv = -1 if controls['axis_4_inv'] else 1
axis_5_inv = -1 if controls['axis_5_inv'] else 1

# Open output port.
if port == '':
    outport = mido.open_output()
else:
    outport = mido.open_output(port)

# Show program window.
screen = pygame.display.set_mode([320, 180])
pygame.display.set_caption("midiBox360")

if os.path.isfile(logo):
    logo = pygame.image.load(logo)
    screen.blit(logo, (0,0))
    pygame.display.flip()

if pygame.joystick.get_count():
    joystick = pygame.joystick.Joystick(joystick_id)
    joystick.init()

clock = pygame.time.Clock()

done = False

# Main program loop.
while done==False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        # Move base note up or down an octave/semitone.
        if event.type == pygame.JOYHATMOTION:
            if get_event(hat_up):
                base_note = (base_note + 12) % 128
            if get_event(hat_down):
                base_note = (base_note - 12) % 128
            if get_event(hat_left):
                base_note = (base_note - 1) % 128
            if get_event(hat_right):
                base_note = (base_note + 1) % 128

        # Detect button presses.
        if event.type == pygame.JOYBUTTONDOWN:
            # Assign joystick events.
            root = get_event(a_button) or get_event(b_button)\
                or get_event(x_button) or get_event(y_button)
            chord = get_event(b_button) or get_event(x_button)
            seventh = get_event(b_button)
            set_mode = get_event(y_button)
            chord_mode = get_event(l_thumb)
            maj_chord = get_event(y_button)
            min_chord = get_event(a_button)
            dom_chord = get_event(b_button)
            dim_chord = get_event(x_button)

            play = 0
            octave = 0
            semitone = 0
            # Define note to be played.
            if get_event(l_trigger):
                play += 1
            if get_event(l_bumper):
                play += 2
            if get_event(r_bumper):
                play += 4
            if get_event(l_stick_up):
                octave = 1
            if get_event(l_stick_down):
                octave = -1
            if get_event(l_stick_left):
                semitone = -1
            if get_event(l_stick_right):
                semitone = 1

            if not playing and root:
                if not chord_mode:
                    # Play diationic chords.
                    if set_mode:
                        mode = play % 7
                        base_note = config['base_note'] - notes[mode]
                    else:
                        outport.send(msg(0, semitone))
                        if chord:
                            outport.send(msg(2, semitone))
                            outport.send(msg(4, semitone))
                        if seventh:
                            outport.send(msg(6, semitone))
                else:
                    # Play specific chord quality.
                    if maj_chord:
                        outport.send(msg(0,0 + semitone))
                        outport.send(msg(0,4 + semitone))
                        outport.send(msg(0,7 + semitone))
                    elif min_chord:
                        outport.send(msg(0,0 + semitone))
                        outport.send(msg(0,3 + semitone))
                        outport.send(msg(0,7 + semitone))
                    elif dom_chord:
                        outport.send(msg(0,0 + semitone))
                        outport.send(msg(0,4 + semitone))
                        outport.send(msg(0,7 + semitone))
                        outport.send(msg(0,10 + semitone))
                    elif dim_chord:
                        outport.send(msg(0,0 + semitone))
                        outport.send(msg(0,3 + semitone))
                        outport.send(msg(0,6 + semitone))
                        outport.send(msg(0,9 + semitone))
                playing = True

        if event.type == pygame.JOYBUTTONUP:
            # Release all notes.
            playing = False
            for i in range(0, 127):
                outport.send(mido.Message('note_off',
                            channel=channel, note=i))

    clock.tick(30)

outport.close()
pygame.quit()
