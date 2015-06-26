# scaling-indicator
AppIndicator for monitoring and changing GNOME's text-scaling-factor. 
Useful for laptops with a HiDPI screen, switching between external displays of varying DPIs and projectors.
Until Wayland's automated support of per-display configuration, I find this useful when switching displays.

# Prerequisites
scaling-indicator depends on GNOME's AppIndicator extension, as well as python's AppIndicator and watchdog library.

GNOME extension: https://extensions.gnome.org/extension/615/appindicator-support/

sudo apt-get install python-appindicator

sudo pip install watchdog

# Installation

(Optional) Modify scaling-indicator.py, in the OPTIONS area, add your favorite or most used scaling settings

chmod a+x setup.sh

sudo ./setup.sh

Log in and log back out, or manually run /usr/bin/scaling-indicator.py

# Removal

rm ~/.config/autostart/scaling-indicator.desktop

sudo rm /usr/bin/scaling-indicator.py

sudo rm -R /usr/lib/scalingindicator

# Use

Click the AppIndicator to change scaling setting, use "Custom..." to input one not shown on the list.

I recommend setting hotkeys in GNOME for your most used settings. For example, I use 

Control+Alt+1 : 1.0

Control+alt+2 : 1.2

Control+Alt+8 : 0.8

When changing scaling by hotkey, or with GNOME's tweak tool, the AppIndicator should update within 2 seconds to show the current setting.

To modify the options shown in the dropdown, edit /usr/bin/scaling-indicator.py (as root) and edit the OPTIONS array near the top of the code. Log out and log in, or restart the process manually.
