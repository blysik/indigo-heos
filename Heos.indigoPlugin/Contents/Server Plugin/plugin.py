#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2017, blysik. All rights reserved.

import os
import sys
import re
import traceback
import indigo
import indigoPluginUpdateChecker
sys.path.append('./lib')
import heos


class Plugin(indigo.PluginBase):

    ##########################################################################
    # class init & del
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(
            self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get("showDebugInfo", False)
        versionFileUrl = "https://raw.githubusercontent.com/blysik/indigo-heos/master/VersionInfo.html"
        self.updater = indigoPluginUpdateChecker.updateChecker(
            self, versionFileUrl)
        self.devices = {}
        self.refresh_speaker_list()

    def __del__(self):
        indigo.PluginBase.__del__(self)

    ##########################################################################
    # plugin startup and shutdown
    def startup(self):
        self.debugLog(u"Method: startup")
        self.updater.checkVersionPoll()

    def shutdown(self):
        self.debugLog(u"Method: shutdown")

    ##########################################################################
    # ConcurrentThread: Start & Stop
    def runConcurrentThread(self):
        self.debugLog(u"Method: runConcurrentThread")
        try:
            self.updater.checkVersionPoll()
            while True:
                for devId in self.devices.keys():
                    self.updateStatus(devId)
                self.sleep(2)
        except self.StopThread:
            return
        except Exception as e:
            self.logger.error("runConcurrentThread error: \n%s" %
                              traceback.format_exc(10))

    def deviceStartComm(self, dev):
        self.debugLog(u"Method: deviceStartComm")
        pid = dev.pluginProps['pid']
        ip = 'blank'
        for i in self.speakers:
            if str(i['pid']) == pid:
                ip = i['ip']
                break
        dev.updateStateOnServer('ip', value=ip)
        heos_obj = heos.Heos(host=ip, verbose=False)
        heos_obj._player_id = pid
        devTup = (dev, heos_obj)
        self.devices[dev.id] = devTup
        self.updateStatus(dev.id)

    def deviceStopComm(self, dev):
        self.debugLog(u"Method: deviceStopComm")
        try:
            del self.devices[dev.id]
        except:
            pass

    def checkForUpdates(self):
        indigo.server.log(u"Manually checking for updates")
        self.updater.checkVersionNow()

    def closedPrefsConfigUi(self, valuesDict, userCancelled):
        # Since the dialog closed we want to set the debug flag - if you don't directly use
        # a plugin's properties (and for debugLog we don't) you'll want to translate it to
        # the appropriate stuff here.
        if not userCancelled:
            self.debug = valuesDict.get("showDebugInfo", False)
            if self.debug:
                indigo.server.log("Debug logging enabled")
            else:
                indigo.server.log("Debug logging disabled")

    ###############
    # updateStatus
    #
    # Updates the status for the specified device.
    ###############
    def updateStatus(self, dev_id):
        devTup = self.devices.get(dev_id, None)
        if devTup:
            dev = devTup[0]
            heos_obj = devTup[1]
            gps = heos_obj.get_play_state()
            if gps == 'play':
                p_gps = 'playing'
            elif gps == 'stop':
                p_gps = 'stopped'
            elif gps == 'pause':
                p_gps = 'paused'
            gms = heos_obj.get_mute_state()
            gv = heos_obj.get_volume()
            media = heos_obj.get_now_playing_media()
            state_list = [
                {"key": "volume", "value": gv},
                {"key": "playStatus", "value": p_gps},
                {"key": "muteStatus", "value": gms},
                {"key": "media-album", "value": media['album']},
                {"key": "media-artist", "value": media['artist']},
                {"key": "media-qid", "value": media['qid']},
                {"key": "media-song", "value": media['song']},
                {"key": "media-album_id", "value": media['album_id']},
                {"key": "media-station", "value": media['station']},
                {"key": "media-image_url", "value": media['image_url']},
                {"key": "media-sid", "value": media['sid']},
                {"key": "media-type", "value": media['type']}
            ]
            dev.updateStatesOnServer(state_list)
            if gps == 'play':
                dev.updateStateImageOnServer(indigo.kStateImageSel.AvPlaying)
            elif gps == 'stop':
                dev.updateStateImageOnServer(indigo.kStateImageSel.AvStopped)
            elif gps == 'pause':
                dev.updateStateImageOnServer(indigo.kStateImageSel.AvPaused)

    def refresh_speaker_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        heos_object = heos.Heos(verbose=False)
        self.speakers = heos_object.get_players()
        self.logger.debug("speakers list: %s" % unicode(self.speakers))

    #################################
    # Config dialog methods
    ##################################
    ###############
    # get_receiver_list
    #
    # Returns the list of speakers as a tuple for the device config dialog.
    ###############
    def get_speaker_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        dialog_list = []
        for i in self.speakers:
            dialog_list.append([str(i['pid']), i['name']])
        return dialog_list

    def speakerSelected(self, valuesDict, typeId, devId):
        self.selectedSpeaker = valuesDict['txtspid']

    def get_input_list(self, filter="", valuesDict=None, typeId="", targetId=0):
        try:
            self.selectedSpeaker
        except AttributeError:
            self.logger.debug("self.selectedSpeaker is not set, trying again")
            return []
        else:
            self.logger.debug("Generating speaker input list")
            heos_object = heos.Heos(verbose=False)
            inputs_list = []
            inputs_reply = heos_object.get_browse_source(self.selectedSpeaker)
            self.logger.debug(inputs_reply)
            for i in inputs_reply:
                inputs_list.append([i['mid'], i['name']])
            return inputs_list

    ##########################################################################
    # Action Menthods

    def actionPlay(self, pluginAction, dev):
        self.logger.debug(u"actionPlay called")
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        heos_obj.play()
        self.updateStatus(dev.id)

    def actionPause(self, pluginAction, dev):
        self.logger.debug(u"actionPause called")
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        heos_obj.pause()
        self.updateStatus(dev.id)

    def actionStop(self, pluginAction, dev):
        self.logger.debug(u"actionStop called")
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        heos_obj.stop()
        self.updateStatus(dev.id)

    def setVolume(self, pluginAction, dev):
        self.logger.debug(u"setVolume called")
        val = int(pluginAction.props['txtvolume'])
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        level = heos_obj.set_volume(val)  # set volume takes integer
        self.logger.debug(level)
        self.updateStatus(dev.id)

    def actionVolumeDown(self, pluginAction, dev):
        self.logger.debug(u"actionVolumeDown called")
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        heos_obj.volume_level_down
        self.updateStatus(dev.id)

    def actionVolumeUp(self, pluginAction, dev):
        self.logger.debug(u"actionVolumeUp called")
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        heos_obj.volume_level_up
        self.updateStatus(dev.id)

    def toggleMute(self, pluginAction, dev):
        self.logger.debug(u"toggleMute called")
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        heos_obj.toggle_mute
        self.updateStatus(dev.id)

    def playInputOther(self, pluginAction, dev):
        self.logger.debug(u"playInputOther called")
        spid = pluginAction.props['txtspid']
        input = pluginAction.props['txtinput']
        dev, heos_obj = self.devices.get(dev.id, (None, None))
        reply = heos_obj.play_input_other(spid, input)
        self.logger.debug(reply)
        self.updateStatus(dev.id)

    ##########################################################################
    # Menu Items

    ##########################################################################
    # Lists for UI
