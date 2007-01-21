#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, math, stat
from libavg import avg
from libavg import anim

global gCalibrator
global gPlayer

class Calibrator:
    def __init__(self, Tracker, Player):
        global gCalibrator
        global gPlayer
        gPlayer = Player
        gCalibrator = self
        self.__isActive = False
        self.__Tracker = Tracker
        self.__ParamList = [
            {'Name':"threshold", 'min':1, 'max':255, 'increment':1, 'precision':0},
            {'Name':"brightness", 'min':1, 'max':255, 'increment':1, 'precision':0},
            {'Name':"gamma", 'min':0, 'max':1, 'increment':1, 'precision':0},
            {'Name':"shutter", 'min':1, 'max':533, 'increment':1, 'precision':0},
            {'Name':"gain", 'min':16, 'max':64, 'increment':1, 'precision':0},
            {'Name':"trapezoid", 'min':0, 'max':1, 'increment':0.01, 'precision':2},
            {'Name':"barrel", 'min':0, 'max':2, 'increment':0.01, 'precision':2},
            {'Name':"left", 'id':"roileft", 'min':0, 'max':320, 'increment':1, 'precision':0},
            {'Name':"top", 'id':"roitop", 'min':0, 'max':240, 'increment':1, 'precision':0},
            {'Name':"right", 'id':"roiright", 'min':320, 'max':640, 'increment':1, 'precision':0},
            {'Name':"bottom", 'id':"roibottom", 'min':240, 'max':480, 'increment':1, 'precision':0}
        ]
        for Param in self.__ParamList:
            if not('id' in Param):
                Param['id'] = Param['Name']
        self.__curParam = 0
        self.__saveIndex = 0
    def __flipBitmap(self, ImgName):
        Node = gPlayer.getElementByID(ImgName)
        for y in range(Node.getNumVerticesY()):
            for x in range(Node.getNumVerticesX()):
                pos = Node.getOrigVertexCoord(x,y)
                pos.y = 1-pos.y
                Node.setWarpedVertexCoord(x,y,pos)
    def __updateBitmap(self, ImgName, TrackerID):
        Bitmap = self.__Tracker.getImage(TrackerID)
        Node = gPlayer.getElementByID(ImgName)
        Node.setBitmap(Bitmap)
        if ImgName != "fingers":
            Node.width=Bitmap.getSize()[0]/4
            Node.height=Bitmap.getSize()[1]/4
        else:
            Node.width = 1278
            Node.height = 718
        self.__flipBitmap(ImgName)
    def __getParam(self, Name):
        return getattr(self.__Tracker, Name)
    def __setParam(self, Name, Val):
        setattr(self.__Tracker, Name, Val)
    def __displayParams(self):
        i = 0
        for Param in self.__ParamList:
            Node = gPlayer.getElementByID("param"+str(i))
            Name = Param['id']
            Val = self.__getParam(Name)
            Node.text = Param['Name']+": "+('%(val).'+str(Param['precision'])+'f') % {'val': Val}
            if self.__curParam == i:
                Node.color = "FFFFFF"
            else:
                Node.color = "A0A0FF"
            i += 1
    def __changeParam(self, Change):
        curParam = self.__ParamList[self.__curParam]
        Val = self.__getParam(curParam['id'])
        Val += Change*curParam['increment']
        if Val < curParam['min']:
            Val = curParam['min']
        if Val > curParam['max']:
            Val = curParam['max']
        self.__setParam(curParam['id'], Val)
    def onFrame(self):
        self.__updateBitmap("camera", avg.IMG_CAMERA)
        self.__updateBitmap("distorted", avg.IMG_DISTORTED)
        self.__updateBitmap("nohistory", avg.IMG_NOHISTORY)
        self.__updateBitmap("histogram", avg.IMG_HISTOGRAM)
        self.__updateBitmap("fingers", avg.IMG_FINGERS)
    def switchActive(self):
        global gPlayer
        if self.__isActive:
            self.__isActive = False
            gPlayer.getElementByID("calibrator").active = 0
            gPlayer.getElementByID("calibrator").opacity = 0
            gPlayer.clearInterval(self.__onFrameID)
        else:
            self.__isActive = True
            gPlayer.getElementByID("calibrator").active = 1 
            gPlayer.getElementByID("calibrator").opacity = 1 
            self.__onFrameID = gPlayer.setInterval(1, self.onFrame)
            self.__displayParams()
        self.__Tracker.debug = self.__isActive
    def onKeyUp(self, Event):
        if Event.keystring == "up":
            if self.__curParam > 0:
                self.__curParam -= 1
        elif Event.keystring == "down":
            if self.__curParam < len(self.__ParamList)-1:
                self.__curParam += 1
        elif Event.keystring == "left":
            self.__changeParam(-1)
        elif Event.keystring == "right":
            self.__changeParam(1)
        elif Event.keystring == "page up":
            self.__changeParam(-10)
        elif Event.keystring == "page down":
            self.__changeParam(10)
        elif Event.keystring == "h":
            self.__Tracker.resetHistory()
            print "History reset"
        elif Event.keystring == "s":
            self.__Tracker.saveConfig()
            print ("Tracker configuration saved.")
        elif Event.keystring == "w":
            self.__saveIndex += 1
            self.__Tracker.getImage(avg.IMG_CAMERA).save("img"+str(self.__saveIndex)+"_camera.png")
            self.__Tracker.getImage(avg.IMG_DISTORTED).save("img"+str(self.__saveIndex)+"_distorted.png")
            self.__Tracker.getImage(avg.IMG_NOHISTORY).save("img"+str(self.__saveIndex)+"_nohistory.png")
            self.__Tracker.getImage(avg.IMG_HIGHPASS).save("img"+str(self.__saveIndex)+"_highpass.png")
            self.__Tracker.getImage(avg.IMG_FINGERS).save("img"+str(self.__saveIndex)+"_fingers.png")
            print ("Images saved.")
        else:
            print "Unknown key ", Event.keystring
        self.__displayParams()
    def isActive(self):
        return self.__isActive

def onTouchDown():
    Event = gPlayer.getCurEvent()
    Node = gPlayer.getElementByID("cursor") 
    Node.x = Event.x-8
    Node.y = Event.y-8
