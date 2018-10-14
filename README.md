# midiBox360

midiBox360 turns an Xbox 360 controller into a MIDI controller that can be used
on any DAW. It works on Linux and Windows. It may run on other platforms, but it
hasn't been tested.

## Getting Started

To get midiBox360, clone this repository or simply download the
midiBox360.py file.

### Prerequisites

In order to run midiBox360, you will need to install the latest version of
Python, and the modules `toml`, `mido`, and `pygame`. Make sure to add Python to
your PATH enviroment variable when you install it. You can install the required
modules by running the following commands:

```
$ pip install toml
$ pip install mido
$ pip install pygame
```

On Windows, you may need to run `cmd` with Administrator privileges before
running these commands.

### Installing

There is no installer for midiBox360 as of now. It needs to be run from source.

## Configuring midiBox360

When you first run midiBox360, it will generate a configuration file
`config.toml` in "%LOCALAPPDATA%/midiBox360" on Windows and
"~/.condig/midiBox360" on Linux, which you can edit with your preferred text
editor. The file contains information on what each setting does; you don't need
to change most of them, but it's important to note that if you want to be able
to use with any DAW on Windows, you will need to install a virtual MIDI cable
(I personally recommend
[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)) and type the
name of the appropriate port in the `port` setting (i.e. "loopMIDI Port").

midiBox360 doesn't have a proper GUI as of yet. It just opens a small empty
window for the sake of making it possible to close it.

### Using the Xbox 360 Controller

midiBox360 will play a note when you press the A face button on the Xbox360
controller. You can play different notes by holding different combinations of
the left trigger (LT) and the shoulder buttons (LB and RB). Each combination
corresponds to a scale degree, as follows:

```
        None = 1
          LT = 2
          LB = 3
     LT + LB = 4
          RB = 5
     RB + LT = 6
     RB + LB = 7
LT + LB + RB = 8 (1 + one octave)
```

Pressing the X face button will play a chord instead of a single note. B will
play a 7th chord.

Holding left or right on the left stick will play notes one octave lower or
higher, respectively.

Pressing up and down on the D-pad moves the base octave up and down, and
pressing right and left moves the base note one semitone up or down,
respectively.

Pressing the Y face button will change the current mode you're playing in into
the mode corresponding to the scale degree equivalent to the combination of LT,
LB and RB being held down.

**NOTE:** Since `pygame` uses DirectInput on Windows, both triggers are assigned
the same axis, which makes it impossible to detect if both are being pressed at
the same time (pressing both gives the same output as pressing none). As a
result, I decided not to assign any function to the right trigger as of now.

Due to this limitation, if I decide to give the right trigger a function in the
future, it will have to be something that doesn't require it to be pressed at
the same time as the left one so as to keep functionality the same on all
platforms.

### Using Other Controllers

The configuration file allows full remapping of the controller, so in theory you
can use any controller you want with midiBox360, not just an Xbox 360 one, as
long as you can find out which value correspond to each button/axis on your
controller*. Bear in mind midiBox360, as the name implies, was made with the
Xbox 360 controller in mind, so it may not work properly with other controllers.

\*The "test" tab on the "controller properties" window on Windows counts
starting from 1, while Python counts starting from 0, so you have to subtract 1
from the ID of the button you want to map when putting it into the config file.

## Notes

midiBox360 is just a silly little personal project of mine, born out of
frustration caused by the lack of a decent way to turn a gamepad into a proper
MIDI controller. The way the program behaves is tailored to my own personal
needs, but I hope it may be useful to someone else.
