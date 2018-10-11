#!/usr/bin/env python3

import toml
import mido
import pygame

default_config = """
# Choose which port midiBox360 ouputs to. Must be inside quotation marks
# An empty string can be used to choose the system's default port
port = ""

# Select a mode to play in based on scale degree. Can be a number from 1 to 7
# 1 = ionian (major); 2 = dorian; 3 = phrygyan; 4 = lydian; 5 = mixolydian;
# 6 = aeolian (minor); 7 = locrian
mode = 1

# Select a MIDI channel to output to. Can be a number from 1 to 16
channel = 4

# Select a note to be used as the root note. Can be a number from 0 to 127
# 60 = middle C
base_note = 60
"""

try:
    config_file = open('config.toml', 'r')
    config = toml.load(config_file)
except FileNotFoundError:
    config = toml.loads(default_config)
    with open('config.toml', 'w', encoding="utf-8") as f:
        f.write(default_config.lstrip())

mido.set_backend('mido.backends.pygame')
pygame.init()
pygame.joystick.init()

notes = [0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28,29,31,33,35,\
         36,38,40,41,43,45,47,48,50,52,53,55,57,59,60,62,64,65,67,69,71,\
         72,74,76,77,79,81,83,84,86,88,89,91,93,95,96,98,100,101,103,105,107,\
         108,110,112,113,115,117,119,120,122,124,125,127]
mode = config['mode'] - 1
channel = config['channel'] - 1
base_note = config['base_note'] - notes[mode]
port = config['port']
octave = 0

if port == '':
    outport = mido.open_output()
else:
    outport = mido.open_output(port)

done = False
screen = pygame.display.set_mode([256, 128])
pygame.display.set_caption("midiBox360")

def msg (add):
    return mido.Message('note_on', channel=channel, note=(base_note +\
                        12 * octave + notes[play + add + mode]) % 128)

while done==False:
    joystick_count = pygame.joystick.get_count()

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    for event in pygame.event.get():
        root = joystick.get_button(0) or joystick.get_button(1)\
               or joystick.get_button(2)
        chord = joystick.get_button(1) or joystick.get_button(2)
        seventh = joystick.get_button(1)
        set_mode = joystick.get_button(3)

        play = 0
        octave = 0
        if joystick.get_axis(2) > 0.8:
            play += 1
        if joystick.get_button(4) == 1:
            play += 2
        if joystick.get_button(5) == 1:
            play += 4
        if joystick.get_axis(0) > 0.8:
            octave = 1
        if joystick.get_axis(0) < -0.8:
            octave = -1

        if event.type == pygame.QUIT:
            done=True

        if event.type == pygame.JOYHATMOTION:
                if joystick.get_hat(0) == (1,0):
                    base_note = (base_note + 1) % 128
                if joystick.get_hat(0) == (-1,0):
                    base_note = (base_note - 1) % 128
                if joystick.get_hat(0) == (0,1):
                    base_note = (base_note + 12) % 128
                if joystick.get_hat(0) == (0,-1):
                    base_note = (base_note - 12) % 128

        if event.type == pygame.JOYBUTTONDOWN:
            if root:
                outport.send(msg(0))
            if chord:
                outport.send(msg(2))
                outport.send(msg(4))
            if seventh:
                outport.send(msg(6))
            if set_mode:
                mode = play % 7
                base_note = config['base_note'] - notes[mode]

        if event.type == pygame.JOYBUTTONUP:
            for i in range(0, 127):
                outport.send(mido.Message('note_off', channel=channel, note=i))

pygame.quit()
