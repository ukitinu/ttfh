# Till the Final Hour

<img align="right" src="https://user-images.githubusercontent.com/52630493/149021546-af2f26f3-001c-4e42-b673-099292d1347e.png" height="400">

Graphical clock to cycle over three days, made for a p&amp;p campaign loosely inspired by *TLOZ: Majora's Mask*.

As in Majora's Mask, each day starts at 05:00.  
The clock can be paused, two play speeds are supported, and there are forward, backward and reset buttons.  
It is possible to store multiple times and load them at a later time: useful if the party decides to split and the
players don't spend the same amount of time. These savestates are deleted when the clock reset.

**Sound effects are supported.**  
Clock tower bells at certain hours, hour transitions, day transitions, and last day's quakes/rumbles are supported and
can be configured.  
**Sound effects are not supplied.**  
I use some of the original sound effects, which means, since it's well known that Nintendo hates their fans, that I
won't share them. You can supply your own MP3s, or you can leave it as is so that no sound plays.

<br>

## Configuration and execution

1. Ensure you've got *python3* and *pip* installed on your device.
2. Clone the project/download the files (you may ignore the *.githooks/*, *.github/* and *tests/* directories).
3. Run `pip install -r requirements.txt`.
4. Remove the *.sample* suffix from `ttfh.ini.sample`.
5. Remove the *.sample* suffix from either `run.sh.sample` or `run.vbs.sample` (depending on your OS), hereinafter
   referred to as `run` file.
6. In `ttfh.ini`, set the value of *python3* (under the *[SYSTEM]* section) to the command that executes python3.
7. In `ttfh.ini`, set the values ending with *-name* in the *[GUI]* section to whatever you want (if that doesn't fit
   the window, you can resize it editing *width* and/or *height*).
8. In `ttfh.ini`, set the values *interval-short* and *interval-long* in the *[TIMER]* section to the duration in
   milliseconds of one in-game minute (default and slow speed) (e.g., if you want a default hour to last 2 minutes,
   set *interval-short* to 2000).
9. Run `make_run.py` to (possibly) update the `run` file.
10. Execute the `run` file and enjoy.
11. If you close the window, the current time is saved, together with all the savestates. Next time you execute
    the `run` file, it will continue from the previous time and the saves will be available.

<br>

### Sounds

In this section you can define your own sound effects.  
*bells* plays every day at the hours listed in *bell-hours* (and minute 0).  
*tick* plays at every hour change that is *not* listed in *bell-hours*.  
*rumble* plays at the hours listed in *rumble-hours*, only during the third (last) day.  
*transition* plays at avery day transition.

### Images

In this section, you can put your own buttons' icons, I recommend keeping them 16x16 in size.

