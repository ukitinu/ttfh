# countdown
Graphical countdown timer made for a p&amp;p campaign loosely inspired by *TLOZ: Majora's Mask*.

**Sound effects are supported, but not supplied.**  
I use some of the original sound effects, which means, since it's well known that Nintendo hates their fans, that I won't
share them. You can supply your own MP3s, or you can leave it as is and have no sounds played.

### Configuration and execution
1. Ensure you've got *python3* and *pip* installed on your device.
2. Run `pip install -r requirements.txt`.
3. Remove the *.sample* suffix from `countdown.ini.sample`.
4. Remove the *.sample* suffix from either `run.sh.sample` or `run.vbs.sample` (depending on your OS), hereinafter referred to as `run` file.
5. In `countdown.ini`, set the value of *python3* (first key in the .ini) to the command that executes python3.
6. In `countdown.ini`, set the values ending with *-name* in the *[LABEL]* section to whatever you want (that fits the window).
7. In `countdown.ini`, set the values *interval-short* and *interval-long* in the *[TIMER]* section to the duration in milliseconds of one game-minute.
8. Run `setup.py` to (possibly) update the `run` file.
9. Execute the `run` file and enjoy.
10. If you close the window, the current time is saved. Next time you execute the `run` file, it will continue from the previous time.

### Advanced configuration
TODO
