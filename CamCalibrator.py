#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, math, stat
from libavg import avg

global gPlayer

class CamCalibrator:
    def __init__(self, Tracker, Player):
        global gPlayer
        gPlayer = Player
        self.__isActive = False
        self.__Tracker = Tracker
        self.__showSmallBmps = True
        self.__ParamList = [
            {'Name':"Track Threshold", 'path':"/tracker/track/threshold/@value", 'min':1, 'max':255, 'increment':1, 'precision':0},
            {'Name':"Touch Threshold", 'path':"/tracker/touch/threshold/@value", 'min':1, 'max':255, 'increment':1, 'precision':0},
            {'Name':"Brightness", 'path':"/camera/brightness/@value", 'min':1, 'max':255, 'increment':1, 'precision':0},
            {'Name':"Shutter", 'path':"/camera/shutter/@value", 'min':1, 'max':533, 'increment':1, 'precision':0},
            {'Name':"Gain", 'path':"/camera/gain/@value", 'min':16, 'max':64, 'increment':1, 'precision':0},
        ]
        self.__curParam = 0
        self.__saveIndex = 0
        self.__onFrameID = gPlayer.setOnFrameHandler(self.onFrame)
    def __flipBitmap(self, ImgName):
        Node = gPlayer.getElementByID(ImgName)
        Grid = Node.getOrigVertexCoords()
        Grid = [ [ (pos[0], 1-pos[1]) for pos in line ] for line in Grid]
        Node.setWarpedVertexCoords(Grid)
    def __updateBitmap(self, ImgName, TrackerID, fullSize = False):
        Bitmap = self.__Tracker.getImage(TrackerID)
        Node = gPlayer.getElementByID(ImgName)
        Node.setBitmap(Bitmap)
        if fullSize:
            Node.width = 1280
            Node.height = 720
        else:
            Node.width=Bitmap.getSize()[0]/4
            Node.height=Bitmap.getSize()[1]/4
#        self.__flipBitmap(ImgName)
    def __getParam(self, Path):
        return int(self.__Tracker.getParam(Path))
    def __setParam(self, Path, Val):
        self.__Tracker.setParam(Path, str(Val))
    def __displayParams(self):
        i = 0
        for Param in self.__ParamList:
            Node = gPlayer.getElementByID("param"+str(i))
            Name = Param['path']
            Val = float(self.__getParam(Name))
            Node.text = Param['Name']+": "+('%(val).'+str(Param['precision'])+'f') % {'val': Val}
            if self.__curParam == i:
                Node.color = "FFFFFF"
            else:
                Node.color = "A0A0FF"
            i += 1
    def __changeParam(self, Change):
        curParam = self.__ParamList[self.__curParam]
        Val = self.__getParam(curParam['path'])
        Val += Change*curParam['increment']
        if Val < curParam['min']:
            Val = curParam['min']
        if Val > curParam['max']:
            Val = curParam['max']
        self.__setParam(curParam['path'], Val)
    def __showImages(self):
        self.__showSmallBmps = not(self.__showSmallBmps) 
        self.__Tracker.setDebugImages(self.__showSmallBmps, True)
        gPlayer.getElementByID("tracking").active = self.__showSmallBmps
    def onFrame(self):
        if self.__showSmallBmps and self.__isActive:
            self.__updateBitmap("camera", avg.IMG_CAMERA)
            self.__updateBitmap("distorted", avg.IMG_DISTORTED)
            self.__updateBitmap("nohistory", avg.IMG_NOHISTORY)
            self.__updateBitmap("histogram", avg.IMG_HISTOGRAM)
            self.__updateBitmap("bkgnd", avg.IMG_DISTORTED, True)
        self.__updateBitmap("fingers", avg.IMG_FINGERS, True)
    def switchActive(self, ShowFingers):
        global gPlayer
        if self.__isActive:
            self.__isActive = False
            gPlayer.getElementByID("camcalibrator").active = 0
            gPlayer.getElementByID("camcalibrator").opacity = 0
#            gPlayer.clearInterval(self.__onFrameID)
        else:
            self.__isActive = True
            gPlayer.getElementByID("camcalibrator").active = 1 
            gPlayer.getElementByID("camcalibrator").opacity = 1 
            self.__displayParams()
        self.__Tracker.setDebugImages(self.__showSmallBmps, 
                self.__isActive or ShowFingers)
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
        elif Event.keystring == "w":
            self.__saveIndex += 1
            self.__Tracker.getImage(avg.IMG_CAMERA).save("img"+str(self.__saveIndex)+"_camera.png")
            self.__Tracker.getImage(avg.IMG_DISTORTED).save("img"+str(self.__saveIndex)+"_distorted.png")
            self.__Tracker.getImage(avg.IMG_NOHISTORY).save("img"+str(self.__saveIndex)+"_nohistory.png")
            self.__Tracker.getImage(avg.IMG_HIGHPASS).save("img"+str(self.__saveIndex)+"_highpass.png")
            self.__Tracker.getImage(avg.IMG_FINGERS).save("img"+str(self.__saveIndex)+"_fingers.png")
            print ("Images saved.")
        elif Event.keystring == "i":
            self.__showImages()
        else:
            print "Unknown key ", Event.keystring
        self.__displayParams()
    def isActive(self):
        return self.__isActive

def onTouchDown():
    Event = gPlayer.getCurEvent()
    if Event.source != avg.TRACK:
        Node = gPlayer.getElementByID("cursor") 
        Node.x = Event.x-8
        Node.y = Event.y-8
