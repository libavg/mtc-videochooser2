#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, stat
from libavg import avg
from libavg import anim
from CamCalibrator import *
from CoordCalibrator import *
from scrollbar import *
from videoinfo import *

BORDER_WIDTH=4
VIDEO_THUMBNAIL_WIDTH=225
VIDEO_THUMBNAIL_HEIGHT=127
#VIDEO_DIR="/home/uzadow/wos_videos/"
#VIDEO_DIR="/home/mtc/"
VIDEO_DIR="/Users/uzadow/wos_videos/"
VIDEO_AREA_WIDTH=1169

ourSelectedVideo = -1
curDir = -1
isSeeking = False

def videoMouseOver():
    Event = Player.getCurEvent()
    if Event.source != avg.TRACK:
        videoIndex = int(Event.node.id[5:])
        Player.getElementByID("videoselected"+str(videoIndex)).opacity=0.5

def videoMouseOut():
    Event = Player.getCurEvent()
    if Event.source != avg.TRACK:
        videoIndex = int(Event.node.id[5:])
        if videoIndex == ourSelectedVideo:
            Player.getElementByID("videoselected"+str(videoIndex)).opacity=0.67
        else:
            Player.getElementByID("videoselected"+str(videoIndex)).opacity=0.0

def videoMouseUp():
    Event = Player.getCurEvent()
    if Event.source != avg.TRACK:
        if Event.node.id[:5] == "video":
            videoIndex = int(Event.node.id[5:])
            selectVideo(videoIndex)

def addControls():
    global seekScrollBar
    seekScrollBar = ScrollBar(Player, Player.getElementByID("videospace"), 25, 370, 
            619, 1000)
    seekScrollBar.setSlider(0.0, 100)
    seekScrollBar.setCallbacks(onSeekControlStart, onSeekControlMove, onSeekControlStop)

def onSeekControlStart(pos):
    global isSeeking
    isSeeking = True
    onSeekControlMove(pos)

def onSeekControlMove(pos):
    if pos == 0:
        pos = 1
    if ourSelectedVideo != -1:
        Player.getElementByID("mainvideo").seekToFrame(int(pos))
        Player.getElementByID("video"+str(ourSelectedVideo)).seekToFrame(int(pos))
    
def onSeekControlStop():
    global isSeeking
    isSeeking = False

def setSeekScrollBar():
    global seekScrollBar
    ourVideo = Player.getElementByID("video"+str(ourSelectedVideo))
    seekScrollBar.setRange((ourVideo.getNumFrames()*31)/30+1)
    seekScrollBar.setSlider(ourVideo.getCurFrame(), ourVideo.getNumFrames()/30+1)

def initVideoNodes():
    global Player
    global curVideoInfos
    def createVideoNode(index, href, title):
        videoDiv = Player.createNode("<div id='videodiv"+str(index)+"'/>")
        videoDiv.x = (VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2)*index
        Player.getElementByID("videos").addChild(videoDiv)
        
        node = Player.createNode("<image id='videoselected"+str(index)+
                "' href='images/VideoSelected.png'/>")
        node.y = 22
        node.width = VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2
        node.height = VIDEO_THUMBNAIL_HEIGHT+BORDER_WIDTH*2
        node.opacity = 0
        videoDiv.addChild(node)
        
        node = Player.createNode("<video id='video"+str(index)+"' href='"+href+
                "' loop='true' threaded='True' oncursorover='videoMouseOver' oncursorout='videoMouseOut' "
                "oncursorup='videoMouseUp'/>")
        node.x = 0 
        node.y = (VIDEO_THUMBNAIL_HEIGHT-(VIDEO_THUMBNAIL_WIDTH*3/4))/2
        node.height = VIDEO_THUMBNAIL_WIDTH*3/4
        node.width = VIDEO_THUMBNAIL_WIDTH
        cropDiv = Player.createNode("<div id='crop"+str(index)+"'/>")
        cropDiv.x = BORDER_WIDTH
        cropDiv.y = 19+BORDER_WIDTH
        cropDiv.height = VIDEO_THUMBNAIL_HEIGHT
        cropDiv.width = VIDEO_THUMBNAIL_WIDTH
        cropDiv.addChild(node)
        videoDiv.addChild(cropDiv)

        node = Player.createNode("<words/>")
        node.x = BORDER_WIDTH+2
        node.y = 3 
        node.size = 14
        node.font = "EurostileCondensed" 
        node.color = "F39C01"
        node.text = title
        videoDiv.addChild(node)
        
    curEntry = 0
    for videoInfo in curVideoInfos:
        href = VIDEO_DIR+ourDirInfos[curDir].dirName+"/"+videoInfo.videoFile
        createVideoNode(curEntry, href, videoInfo.title)
        curEntry += 1

def removeVideoNodes():
    VideoArea = Player.getElementByID("videos")
    for i in range(0, VideoArea.getNumChildren()):
        VideoArea.removeChild(0)

def startVideos():
    global isSeeking
    global CamCal
    if not(CamCal.isActive()):
        VideoArea = Player.getElementByID("videos")
        MainVideo = Player.getElementByID("mainvideo")
        for i in range(0, VideoArea.getNumChildren()):
            CurVideoArea = VideoArea.getChild(i)
            CurVideo = CurVideoArea.getChild(1).getChild(0)
            videoPos = (VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2)*i-sb.getPos()
            if i == ourSelectedVideo:
                if isSeeking:
                    CurVideo.pause()
                    MainVideo.pause()
                else:
                    CurVideo.play()
                    MainVideo.play()
            elif videoPos > -VIDEO_THUMBNAIL_WIDTH and videoPos < 1024:
                CurVideo.play()
            else:
                CurVideo.pause()

def selectVideo(selectedVideo):
    global ourSelectedVideo
    global curVideoInfos
    if ourSelectedVideo != selectedVideo:
        if ourSelectedVideo != -1:
            Player.getElementByID("videoselected"+str(ourSelectedVideo)).opacity=0.0
        ourSelectedVideo = selectedVideo
        Player.getElementByID("videoselected"+str(ourSelectedVideo)).opacity=0.67
        mainVideo = Player.getElementByID("mainvideo")
        smallVideo = Player.getElementByID("video"+str(ourSelectedVideo))
        mainVideo.href=VIDEO_DIR+ourDirInfos[curDir].dirName+"/"+curVideoInfos[ourSelectedVideo].videoFile
        mainVideo.play()
        mainVideo.seekToFrame(smallVideo.getCurFrame())

def selectDir(index):
    global curDir
    global curVideoInfos
    global sb
    global ourSelectedVideo
    if curDir != index:
        if curDir != -1:
            removeVideoNodes()
        curDir = index
        curVideoInfos = ourDirInfos[curDir].videoInfos
        initVideoNodes()
        sb.setRange(getVideoViewportWidth()-14)
        sb.setSlider(0, VIDEO_AREA_WIDTH)
        ourSelectedVideo = -1
        mainVideo = Player.getElementByID("mainvideo")
        mainVideo.href = ""

def onFrame():
    global sb
    global ourSelectedVideo
    if curDir == -1:
        selectDir(0)
    VideoArea = Player.getElementByID("videos")
    VideoArea.x = -sb.getPos()
    startVideos()
    if ourSelectedVideo != -1:
        mainVideo = Player.getElementByID("mainvideo")
        if mainVideo.getCurFrame() == 0:
            newSelectedVideo = ourSelectedVideo+1
            if newSelectedVideo >= VideoArea.getNumChildren():
                newSelectedVideo = 0
            smallVideo = Player.getElementByID("video"+str(newSelectedVideo))
            smallVideo.seekToFrame(1)
            selectVideo(newSelectedVideo)
        setSeekScrollBar()

def getVideoViewportWidth():
    global curVideoInfos
    return len(curVideoInfos)*(VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2)

def activateFingers():
    global Tracker
    global ShowFingers
    if ShowFingers:
        Player.getElementByID("fingers").active = 1
    else:
        Player.getElementByID("fingers").active = 0
    Tracker.setDebugImages(False, ShowFingers)
    
def onKeyUp():
    global CamCal
    global CoordCal
    global Player
    global ShowFingers
    global Tracker
    Event = Player.getCurEvent()
    if Event.keystring == "t":
        CamCal.switchActive(ShowFingers)
        if CamCal.isActive():
            VideoArea = Player.getElementByID("videos")
            for i in range(0, VideoArea.getNumChildren()):
                CurVideoArea = VideoArea.getChild(i)
                CurVideo = CurVideoArea.getChild(1).getChild(0)
                CurVideo.pause()
            mainVideo = Player.getElementByID("mainvideo")
            if mainVideo.href != "":
                mainVideo.pause()
            Player.getElementByID("fingers").active = 1
        else:
            activateFingers()
    elif Event.keystring == "s":
        Tracker.saveConfig()
        print ("Tracker configuration saved.")
    elif Event.keystring == "c":
        if not(CamCal.isActive()) and not(CoordCal):
            CoordCal = CoordCalibrator(Tracker, Player)
    elif Event.keystring == "f":
        ShowFingers = not(ShowFingers)
        if not(CamCal.isActive()):
            activateFingers()
    elif CamCal.isActive():
        CamCal.onKeyUp(Event)
    elif CoordCal:
        Ok = CoordCal.onKeyUp(Event)
        if not(Ok):
            CoordCal = None

Cursors = {}

def onTouchDown():
    pass
#    global CamCal
#    global Player
#    Event = Player.getCurEvent()
#    if CamCal.isActive():
#        c_id = "cursor%s"%Event.cursorid
#        node = Cursors[Event.cursorid] = Player.createNode("<div><words text='%s'/><image href='../images/Cursor.png' id='%s'/></div>"%(c_id,c_id))
#        node.x = Event.x-8
#        node.y = Event.y-8
#        Player.getElementByID('camcalibrator').addChild(node)
        
def onTouchUp():
    pass
#    global CamCal
#    global Player
#    Event = Player.getCurEvent()
#    if CamCal.isActive():
#        try:
#            node = Cursors[Event.cursorid]
#        except KeyError:
#            return
#        calnode = Player.getElementByID('camcalibrator')
#        calnode.removeChild(
#                calnode.indexOf(node))

def onTouchMotion():
    pass
#    global CamCal
#    global Player
#    Event = Player.getCurEvent()
#    if CamCal.isActive():
#        try:
#            node = Cursors[Event.cursorid]
#        except KeyError:
#            return
#        node.x = Event.x-8
#        node.y = Event.y-8

Player = avg.Player()
Log = avg.Logger.get()
bDebug = not(os.getenv('AVG_DEPLOY'))
if (bDebug):
    Player.setResolution(0, 0, 0, 0) 
else:
    Player.setResolution(1, 0, 0, 0)
    Player.showCursor(False)
#    Log.setFileDest("/var/log/cleuse.log")
Log.setCategories(Log.APP |
                  Log.WARNING | 
                  Log.PROFILE |
#                 Log.PROFILE_LATEFRAMES |
                  Log.CONFIG
#                 Log.MEMORY  |
#                 Log.BLTS    
#                 Log.EVENTS| 
#                 Log.EVENTS2
                 )
Player.loadFile("videochooser2.avg")
anim.init(Player)
Player.setFramerate(60)
sb = ScrollBar(Player, Player.getElementByID("videoarea"), 25, 
        35+VIDEO_THUMBNAIL_HEIGHT, VIDEO_AREA_WIDTH-16, 1000)
Player.setOnFrameHandler(onFrame)
addControls()
Tracker = Player.addTracker()
CamCal = CamCalibrator(Tracker, Player)
CoordCal = None
ShowFingers = False;
activateFingers()
Player.play()
Player.getTestHelper().dumpObjects()
