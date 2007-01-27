#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, stat
from libavg import avg
from libavg import anim

global gCoordCal

class CoordCalibrator:
    def __init__(self, Tracker, Player):
        global gPlayer
        gPlayer = Player
        global gCoordCal
        gCoordCal = self
        self.__Tracker = Tracker
        self.__CurPointIndex = 0
        self.__CPPCal = self.__Tracker.startCalibration(1280,720)
        self.__LastCenter = None
        self.__NumMessages = 0
        gPlayer.getElementByID("coordcalibrator").active = True
        gPlayer.getElementByID("coordcalibrator").opacity = 1
        self.__addMessage("Starting calibration.")
        self.__moveMarker()
    def __del__(self):
        gPlayer.getElementByID("coordcalibrator").active = False
        gPlayer.getElementByID("coordcalibrator").opacity = 0
        MsgsNode = gPlayer.getElementByID("messages")
        for i in range(0, MsgsNode.getNumChildren()):
            MsgsNode.removeChild(0)
    def __moveMarker(self):
        Crosshair = gPlayer.getElementByID("crosshair")
        Crosshair.x = self.__CPPCal.getDisplayPointX()-7
        Crosshair.y = self.__CPPCal.getDisplayPointY()-7
        self.__addMessage("Calibrating point "+str(self.__CurPointIndex))
    def __addMessage(self, text):
        MsgsNode = gPlayer.getElementByID("messages")
        if self.__NumMessages > 38:
            for i in range(0, MsgsNode.getNumChildren()-1):
                MsgsNode.getChild(i).text = MsgsNode.getChild(i+1).text
            MsgsNode.removeChild(MsgsNode.getNumChildren()-1)
        else:
            self.__NumMessages += 1
        Node = gPlayer.createNode(
                "<words size='10' font='Eurostile' color='00FF00'/>")
        Node.x = 0
        Node.y = self.__NumMessages*13
        Node.text = text
        MsgsNode.addChild(Node)
    def onTouchUp(self, Event):
        self.__LastCenter = Event.center
        self.__addMessage("  Touch at %(x).2f, %(y).2f" % { "x": Event.center.x, "y": Event.center.y})
    def onKeyUp(self, Event):
        global gCoordCal
        if Event.keystring == "space":
            if self.__LastCenter:
                self.__CPPCal.setCamPoint(self.__LastCenter.x, self.__LastCenter.y)
            self.__LastCenter = None
            Ok = self.__CPPCal.nextPoint()
            self.__CurPointIndex += 1
            self.__moveMarker()
            if not(Ok):
                gCoordCal = None
            return Ok
        elif Event.keystring == "a":
            self.__CPPCal.abort()
            gCoordCal = None
            return False
        return True

def onCoordCalTouchUp():
    global gCoordCal
    Event = gPlayer.getCurEvent()
    gCoordCal.onTouchUp(Event)

