# -*- coding: utf-8 -*-
# Copyright (c) 2013 Paul Price, Artem Glebov

import os
import sys
import xbmc, xbmcaddon, xbmcgui
import transmissionrpc

__settings__ = xbmcaddon.Addon(id='script.transmission')

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __settings__.getAddonInfo('path'), 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

import common

class SubstitutePlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.prev_settings = {}
        self.refreshSettings()

    def onPlayBackStarted(self):
        self.refreshSettings()
        if self.mode != '0' and xbmc.Player().isPlayingVideo():
            if self.mode == '1':
                self.stopAllTorrents()
            elif self.mode == '2':
                self.enableSpeedLimit()

    def onPlayBackStopped(self):
        xbmc.sleep(int(self.seconds))
        self.refreshSettings()
        if self.mode == '1' and not xbmc.Player().isPlayingVideo():
            self.startAllTorrents()
        elif self.mode == '2' and not xbmc.Player().isPlayingVideo():
            self.disableSpeedLimit()		

    def onPlayBackEnded(self):
        xbmc.sleep(self.seconds)	
        self.refreshSettings()
        if self.mode == '1' and not xbmc.Player().isPlayingVideo():
            self.startAllTorrents()
        elif self.mode == '2' and not xbmc.Player().isPlayingVideo():
            self.disableSpeedLimit()			

    def startAllTorrents(self):
        if self.transmission:
            torrents = self.transmission.list()
            for tid, torrent in torrents.iteritems():
                self.transmission.start(tid)

    def stopAllTorrents(self):
        if self.transmission:
            torrents = self.transmission.list()
            for tid, torrent in torrents.iteritems():
                self.transmission.stop(tid)

    def refreshSettings(self):
        settings = common.get_settings()
        if settings != self.prev_settings:
            self.mode = settings['action_on_playback']
            self.seconds = int(settings['seconds_playback_finished'])*1000
            try:
                self.transmission = common.get_rpc_client()
            except:
                self.transmission = None
            self.prev_settings = settings

    def enableSpeedLimit(self):
        if self.transmission:
            self.transmission.set_session(alt_speed_enabled=True)

    def disableSpeedLimit(self):
        if self.transmission:
            self.transmission.set_session(alt_speed_enabled=False)

player = SubstitutePlayer()

while (not xbmc.abortRequested):
    xbmc.sleep(5000);
