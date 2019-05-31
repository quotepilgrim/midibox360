# midiBox360

midiBox360 turns an Xbox 360 controller into a MIDI controller that can be used
on any DAW. It works on Linux and Windows. It may run on other platforms, but it
hasn't been tested.

## Getting started

You can get the latest midiBox360 release on the
[Releases](https://github.com/quotepilgrim/midibox360/releases) page. The binary
release of midiBox360 works out-of-the-box on Windows, with no need to install
anything. Linux users will have to run it from source.

### Prerequisites

In order to run midiBox360 from source, you will need to install the latest
version of Python 3 and the modules `toml`, `mido`, and `pygame`. Make sure
Python is in your PATH environment variable once installed. You can install the
required modules by running the following commands as root/administrator:

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
(I personally recommend [loopMIDI][1]) and type the name of the appropriate port
in the `port` setting (i.e. "loopMIDI Port").

## Listing available MIDI ports

Starting with version 1.2.0, midiBox360 will output a list of all the available
MIDI output ports when ran. You can see that list on Linux simply by running the
program from the terminal. On Windows, open a command prompt in the program's
folder (shift + right-click, then click on "open command window here"), type
`midibox360.exe | more` and hit enter, then close midiBox360's window when it
appears. Once midiBox360 is closed, the list will be displayed in the command
prompt. It should look something like this:

`['Microsoft GS Wavetable Synth', 'Microsoft MIDI Mapper', 'loopMIDI Port']`

If running the program from source on Windows, a command prompt will open itself
and display the list whenever you open the program.

### Using the Xbox 360 controller

midiBox360 will play a note when you press the A face button on the Xbox 360
controller. Which note is played is determined by the combination of shoulder
buttons/triggers being held. Left trigger (LT), left bumper (LB), right bumper
(RB) and right trigger (RT) add 1, 2, 4, and 8 to the note number, respectively.
Here is list of the possible combinations of LT, LB, and RB:

```
        None = 1
          LT = 2
          LB = 3
     LT + LB = 4
          RB = 5
     LT + RB = 6
     LB + RB = 7
LT + LB + RB = 8 (1 + one octave)
```

Holding RT with these combinations will yield the remaining note numbers up
to 16.

Pressing the X face button will play a chord instead of a single note. B will
play a 7th chord.

Holding up or down on the left stick will play notes one octave higher or lower,
and holding right or left will play notes one semitone up or down.

Pressing up and down on the D-pad moves the base note one octave up and down,
and pressing right and left moves the base note one semitone up or down,
respectively.

Pressing the back button toggles a mode where each face
button plays a different chord quality.

Pressing start will change the scale mode to the one
corresponding to the scale degree of the current note (determined by the
combination of shoulder buttons/triggers being held down).
This will also reset the base note.

### Right trigger issue

Due to a limitation in how `pygame` detects inputs, holding both LT and RT down
may not work on Windows. It does work properly on Linux if you set
`right_trigger` to `"axis_5"` in the configuration file, and should work on
Windows with non-Xbox controllers. You can work around this issue either by
changing `right_trigger` to something else, or mapping your controller to a
[vJoy][2] virtual joystick with the help of a tool like [FreePIE][3]. Note that
the program can be used with little to no issue without using the right trigger.

Instructions on the workaround can be found on [the wiki][4].

### Using other controllers

The configuration file allows full remapping of the controller, so you should be
able to use any controller you want with midiBox360 as long as you can find out
which value corresponds to each button/axis on your controller. Bear in mind,
however, that midiBox360 was made with the Xbox 360 controller in mind, so some
may not always work.

For more information and some configuration files, please check [the wiki][4].

## Notes

midiBox360 is just a silly little personal project of mine, born out of
frustration caused by the lack of a decent way to turn a gamepad into a proper
MIDI controller. The way the program behaves is tailored to my own personal
needs, but I hope it may be useful to someone else.

[1]: https://www.tobias-erichsen.de/software/loopmidi.html
[2]: http://vjoystick.sourceforge.net/site/
[3]: https://andersmalmgren.github.io/FreePIE/
[4]: https://github.com/quotepilgrim/midibox360/wiki
