#!/bin/bash

#    Scaling-indicator - AppIndicator for montioring and diplaying GNOME's text-scaling-factor
#    Copyright 2015 Brent Dukes
#
#    This file is part of Scaling-indicator.
#
#    Scaling-indicator is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    Scaling-indicator is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with scaling-indicator.  If not, see <http://www.gnu.org/licenses/>.

if [[ $EUID -ne 0 ]]; then
	echo "This script must be run using sudo" 2>&1
	exit 1
else
	mkdir -p /usr/lib/scalingindicator
	cp scaling-indicator.py /usr/bin/
	chown root:root /usr/bin/scaling-indicator.py
	chmod 755 /usr/bin/scaling-indicator.py
	cp images/*.png /usr/lib/scalingindicator/
	chmod a+r /usr/lib/scalingindicator/*.png

	read -n1 -p "Autostart Scaling Indicator? (y/N) "
	echo $USER
	if [[ $REPLY == [yY] ]]; then
		mkdir -p $HOME/.config/autostart
		cp scaling-indicator.desktop $HOME/.config/autostart
        chown $SUDO_USER:$SUDO_USER $HOME/.config/autostart
        chown $SUDO_USER:$SUDO_USER $HOME/.config/autostart/scaling-indicator.desktop
	else
		rm -f $HOME/.config/autostart/scaling-indicator.desktop
	fi
fi
