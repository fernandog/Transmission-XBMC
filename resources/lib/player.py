# -*- coding: utf-8 -*-
# Copyright (c) 2013 Paul Price, Artem Glebov

import os
import sys
import xbmc, xbmcaddon, xbmcgui
import transmissionrpc
import urllib
import subprocess

__settings__ = xbmcaddon.Addon(id='script.transmission')
__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __settings__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

import common

class SubstitutePlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.prev_settings = {}
        self.refreshSettings()
        self.TimerON = False

    def onPlayBackStarted(self):
        self.refreshSettings()
        if self.mode != '0' and xbmc.Player().isPlayingVideo() == True and self.TimerON == False:
            if self.mode == '1':
                if self.show_notifications == 'true':
                    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Pausing torrents...",5000, __icon__))
                self.stopAllTorrents()
            elif self.mode == '2':
                self.enableSpeedLimit()

    def ResumingTorrents(self):
        xbmc.sleep(1)
        self.refreshSettings()
        if self.mode == '1' and not xbmc.Player().isPlayingVideo():
            if self.show_notifications == 'true':
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Torrents will be started in " + str(self.seconds/1000) + " seconds",5000, __icon__))
        elif self.mode == '2' and not xbmc.Player().isPlayingVideo():
            if self.show_notifications == 'true':
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Speed limited will be disabled in " + str(self.seconds/1000) + " seconds",5000, __icon__))
        self.TimerON = True
        xbmc.sleep(int(self.seconds))
        self.TimerON = False
        if self.mode == '1' and xbmc.Player().isPlayingVideo() == False:
            self.startAllTorrents()
        elif self.mode == '2' and xbmc.Player().isPlayingVideo() == False:
            self.disableSpeedLimit()
        else:
            if self.show_notifications == 'true':
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Still watching. Torrents still paused/limited",5000, __icon__))

    def onPlayBackEnded(self):
        self.ResumingTorrents()

    def onPlayBackStopped(self):    
        self.ResumingTorrents()
            
    def startAllTorrents(self):
        if self.transmission:
            if self.show_notifications == 'true':
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Starting torrents...",5000, __icon__))
            torrents = self.transmission.list()
            for tid, torrent in torrents.iteritems():
                self.transmission.start(tid)

    def stopAllTorrents(self):
        while self.transmission and xbmc.Player().isPlayingVideo() == True:
            torrents = self.transmission.list()
            for tid, torrent in torrents.iteritems():
                if self.keep_seeding == 'true' and torrent.status not in ('seeding'):
                    #print "[Transmission Debug] - Pausing: " + str(torrent.name) + " - " + str(torrent.status)
                    self.transmission.stop(tid)
                elif self.keep_seeding == 'false':
                    #print "[Transmission Debug] - Pausing (All): " + str(torrent.name) + " - " + str(torrent.status)
                    self.transmission.stop(tid)                    
                elif self.keep_seeding == 'true' and torrent.status in ('seeding'):
                    #print "[Transmission Debug] - Not Pausing: " + str(torrent.name) + " - " + str(torrent.status)
                    pass
                else:
                    #print "[Transmission Debug] - None criteria met"
                    pass
            xbmc.sleep(120000)

    def refreshSettings(self):
        settings = common.get_settings()
        if settings != self.prev_settings:
            self.mode = settings['action_on_playback']
            self.keep_seeding = settings['seeding_torrents']
            self.show_notifications = settings['show_notifications']
            self.seconds = int(settings['seconds_playback_finished'])*1000
            try:
                self.transmission = common.get_rpc_client()
            except:
                self.transmission = None
            self.prev_settings = settings

    def enableSpeedLimit(self):
        if self.transmission:
            if self.show_notifications == 'true':
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Enabling speed limit...",5000, __icon__))
            self.transmission.set_session(alt_speed_enabled=True)

    def disableSpeedLimit(self):
        if self.transmission:
            if self.show_notifications == 'true':        
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,"Disabling speed limit...",5000, __icon__))
            self.transmission.set_session(alt_speed_enabled=False)

player = SubstitutePlayer()

while (not xbmc.abortRequested):
    xbmc.sleep(5000);
