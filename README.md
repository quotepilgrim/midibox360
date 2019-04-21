# midiBox360

midiBox360 turns an Xbox 360 controller into a MIDI controller that can be used
on any DAW. It works on Linux and Windows. It may run on other platforms, but it
hasn't been tested.

## Getting Started

You can get the latest midiBox360 release on the
[Releases](https://github.com/quotepilgrim/midibox360/releases) page. The binary
release of midiBox360 works out-of-the-box on Windows, with no need to install
anything. Linux users will have to run it from source.

### Prerequisites

In order to run midiBox360 from source, you will need to install the latest
version of Python 3 and the modules `toml`, `mido`, and `pygame`. Make sure to
add Python is in your PATH environment variable once installed. You can install
the required modules by running the following commands as root/administrator:

```
$ pip install toml
$ pip install mido
$ pip install pygame
```

Once you have all the modules installed, you can launch the `midibox360.py`
script.

## Configuring midiBox360

When you first run midiBox360, it will generate a configuration file
`config.toml` in "%LOCALAPPDATA%/midiBox360" on Windows and
"~/.config/midiBox360" on Linux, which you can edit with your preferred text
editor. The file contains information on what each setting does; you don't need
to change most of them, but it's important to note that if you want to be able
to use it with any DAW on Windows, you will need to install a virtual MIDI cable
(I personally recommend
[loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html)) and type the
name of the appropriate port in the `port` setting (i.e. "loopMIDI Port").

### Using the Xbox 360 Controller

midiBox360 will play a note when you press the A face button on the Xbox360
controller. Which note is played is determined by the combination of shoulder
buttons/triggers being held. Left trigger (LT), left bumper (LB), right bumper
(RB) and right trigger (RT) add 1, 2, 4, and 8 to the note number, respectively.
Here is list of the combinations using LT, LB, and RB.

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

Holding RT with these combinations will yield the remaining note numbers up
to 16.

Pressing the X face button will play a chord instead of a single note. B will
play a 7th chord.

Holding up or down on the left stick will play notes one octave higher or lower,
and holding right or left will play notes one semitone up or down. Pressing the
left stick down makes each face button play a different chord quality.

Pressing up and down on the D-pad moves the base note one octave up and down,
and pressing right and left moves the base note one semitone up or down,
respectively.

Pressing start will change the scale mode to the one corresponding to the
scale degree of the current note (determined by the combination of shoulder
buttons/triggers being held down).

**NOTE:** Combinations with both LT and RT held down won't work on Windows due
to a limitation in `pygame`. It does work properly on Linux, and it may work
on Windows on with some non-Xbox controllers. You can work around this issue by
remapping RT to something else in midiBox360's configuration, or mapping your
controller to a [vJoy](http://vjoystick.sourceforge.net/site/) virtual
joystick and a tool like [FreePIE](https://andersmalmgren.github.io/FreePIE/).
Instructions on how to do that will be linked to here soon.

### Using Other Controllers

The configuration file allows full remapping of the controller, so you should be
able to use any controller you want with midiBox360 as long as you can find out
which value correspond to each button/axis on your controller*. Bear in mind,
however, that midiBox360 was made with the Xbox 360 controller in mind, so this
may no always work.

\*The "test" tab on the "controller properties" window on Windows counts
starting from 1, while Python counts starting from 0, so you have to subtract 1
from the ID of the button you want to map when editing the config file.

## Notes

midiBox360 is just a silly little personal project of mine, born out of
frustration caused by the lack of a decent way to turn a gamepad into a proper
MIDI controller. The way the program behaves is tailored to my own personal
needs, but I hope it may be useful to someone else.
