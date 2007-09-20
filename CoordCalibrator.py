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
        self.__CPPCal = self.__Tracker.startCalibration()
        self.__LastCenter = None
        self.__NumMessages = 0
        self._mycursor = None
        gPlayer.getElementByID("coordcalibrator").active = True
        gPlayer.getElementByID("coordcalibrator").opacity = 1
        self.__addMessage("Starting calibration.")
        self.__moveMarker()
    def __del__(self):
        if gPlayer != None:
            gPlayer.getElementByID("coordcalibrator").active = False
            gPlayer.getElementByID("coordcalibrator").opacity = 0
            MsgsNode = gPlayer.getElementByID("messages")
            for i in range(0, MsgsNode.getNumChildren()):
                MsgsNode.removeChild(0)
    def __moveMarker(self):
        Crosshair = gPlayer.getElementByID("crosshair")
        Crosshair.x, Crosshair.y = self.__CPPCal.getDisplayPoint()
        Crosshair.x, Crosshair.y = (Crosshair.x-7, Crosshair.y-7)
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
        MsgsNode.appendChild(Node)
    def onTouchDown(self, Event):
        if not self._mycursor:
            self._mycursor = Event.cursorid
        else:
            return
        self.__LastCenter = Event.center
        self.__addMessage("  Touch at %(x).2f, %(y).2f" % { "x": Event.center[0], "y": Event.center[1]})
    def onTouchMove(self,Event):
        if self._mycursor == Event.cursorid:
            self.__LastCenter = Event.center

    def onTouchUp(self, Event):
        if self._mycursor:
            self._mycursor = None
        else:
            return

    def onKeyUp(self, Event):
        global gCoordCal
        if Event.keystring == "space":
            if self.__LastCenter:
                self.__CPPCal.setCamPoint(self.__LastCenter)
            self.__LastCenter = None
            Ok = self.__CPPCal.nextPoint()
            self.__CurPointIndex += 1
            self.__moveMarker()
            if not(Ok):
                self.__Tracker.endCalibration()
                gCoordCal = None
            return Ok
        elif Event.keystring == "a":
            self.__Tracker.abortCalibration()
            gCoordCal = None
            return False
        return True

def onCoordCalTouchDown(Event):
    global gCoordCal
    if Event.source != avg.TRACK:
        gCoordCal.onTouchDown(Event)

