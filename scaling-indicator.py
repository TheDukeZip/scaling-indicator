#!/usr/bin/env python

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

import appindicator
import gtk
import os
import commands
import time
import gobject
import decimal
from os.path import expanduser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Populate with common scaling factors you may desire to use
OPTIONS =   [ 
            0.8, 
            1.0, 
            1.25, 
            1.5, 
            2.0
            ]

class FileWatchdogHandler(FileSystemEventHandler):       
    def on_modified(self, event):
        indicator.refresh()

class ScalingIndicator:
    def __init__(self):
        self.ind = appindicator.Indicator("Scaling Indicator",
                                            "/usr/lib/scalingindicator/letters-22.png",
                                            appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)

        self.scalingFactor = self.getScalingFactor()
        self.ind.set_label(self.scalingFactor)

        self.menuSetup()
        self.ind.set_menu(self.menu)

        self.observerSetup()

        self.refresh()

    #Monitor your gsettings file for changes to update indicator
    def observerSetup(self):
        self.observer = Observer()
        self.eventHandler = FileWatchdogHandler()
        self.observer.schedule(self.eventHandler, expanduser("~") + "/.config/dconf", recursive=False)
        self.observer.start()

    #Set up the dropdown menu
    def menuSetup(self):
        self.menu = gtk.Menu()

        #This array will contain all the gtk.CheckMenuItems in the dropdown
        self.options = []

        for option in OPTIONS:
            if len(self.options) == 0:
                group = None
            else:
                group = self.options[0]

            t = gtk.CheckMenuItem(str(option))
            t.set_draw_as_radio(True)
            t.connect("activate", self.setScalingFactor, option)
            t.show()
            self.options.append(t)
            self.menu.append(t)

        self.seperator_item = gtk.SeparatorMenuItem()
        self.seperator_item.show()

        self.custom_item = gtk.MenuItem("Custom...")
        self.custom_item.connect("activate", self.getCustomInput)
        self.custom_item.show()

        self.menu.append(self.seperator_item)
        self.menu.append(self.custom_item)

    def refresh(self):
        self.scalingFactor = self.getScalingFactor()

        #Refresh text next to main icon
        self.ind.set_label(self.scalingFactor)

        #Refresh check marks next to scaling factors in dropdown
        for item in self.options:
            item.set_active(self.scalingFactor == item.get_label())

    def setScalingFactor(self, object, factor):
        if object.get_active():
            os.system("gsettings set org.gnome.desktop.interface text-scaling-factor " + str(factor))
            self.refresh()

    def setScalingFactorCustom(self, factor):
        os.system("gsettings set org.gnome.desktop.interface text-scaling-factor " + str(factor))
        self.refresh()  

    def getScalingFactor(self):
        stat, result = commands.getstatusoutput("gsettings get org.gnome.desktop.interface text-scaling-factor")
        return str(round(float(result), 2))


    def getCustomInput(self, object):
        dialog = gtk.MessageDialog(None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_QUESTION,
                                    gtk.BUTTONS_OK_CANCEL,
                                    None)

        entry = gtk.Entry()
        entry.connect("activate", self.handleCustomInput, dialog, gtk.RESPONSE_OK)

        #create a horizontal box to pack the entry and a label
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Scaling Factor:"), False, 5, 5)
        hbox.pack_end(entry)

        #add it and show it
        dialog.vbox.pack_end(hbox, True, True, 0)
        dialog.show_all()

        dialog.run()
        text = entry.get_text()
        dialog.destroy()

        #Validate this is a valid decimal number before running gsettings with it
        try:
            userInput = decimal.Decimal(text)
            self.setScalingFactorCustom(text)

        except decimal.InvalidOperation:
            dialog = gtk.MessageDialog(None,
                                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                        gtk.MESSAGE_ERROR,
                                        gtk.BUTTONS_OK,
                                        None)
            dialog.set_markup("Please enter a valid decimal number")
            dialog.show_all()
            dialog.run()
            dialog.destroy()

    def handleCustomInput(self, entry, dialog, response):
        dialog.response(response)

    #Kludge to give the thread some cpu time for the file watchdog to trigger if
    # the scaling factor is changed by hotkeys, Gnome Tweak, other apps...
    def timer(self):
        time.sleep(1)
        return True

    def main(self):
        gobject.timeout_add_seconds(2, self.timer)
        gtk.main()

if __name__ == "__main__":
    indicator = ScalingIndicator()
    indicator.main()
