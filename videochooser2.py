#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, math, stat
import avg
import anim
from scrollbar import *
from videoinfo import *

BORDER_WIDTH=16
VIDEO_THUMBNAIL_WIDTH=380
VIDEO_THUMBNAIL_HEIGHT=285
#VIDEO_DIR="/home/uzadow/wos_videos/"
VIDEO_DIR="/Users/uzadow/wos_videos/"
VIDEO_AREA_WIDTH=1842

ourSelectedVideo = -1
curDir = -1

def videoMouseOver():
    Event = Player.getCurEvent()
    videoIndex = int(Event.node.id[5:])
    Player.getElementByID("videoselected"+str(videoIndex)).opacity=0.5
    Player.getElementByID("videounselected"+str(videoIndex)).opacity=0.5

def videoMouseOut():
    Event = Player.getCurEvent()
    videoIndex = int(Event.node.id[5:])
    if videoIndex == ourSelectedVideo:
        Player.getElementByID("videoselected"+str(videoIndex)).opacity=0.67
        Player.getElementByID("videounselected"+str(videoIndex)).opacity=0.0
    else:
        Player.getElementByID("videoselected"+str(videoIndex)).opacity=0.0
        Player.getElementByID("videounselected"+str(videoIndex)).opacity=0.67

def videoMouseUp():
    Event = Player.getCurEvent()
    videoIndex = int(Event.node.id[5:])
    selectVideo(videoIndex)

def initVideoNodes():
    global Player
    global curVideoInfos
    def createVideoNode(index, href, title):
        videoDiv = Player.createNode("<div id='videodiv"+str(index)+"'/>")
        videoDiv.x = (VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2)*index
        Player.getElementByID("videos").addChild(videoDiv)
        
        node = Player.createNode("<image id='videounselected"+str(index)+
                "' href='images/Video.png'/>")
        node.y = 43
        node.width = VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2
        node.height = VIDEO_THUMBNAIL_HEIGHT+BORDER_WIDTH*2
        node.opacity = 0.666
        videoDiv.addChild(node)
        
        node = Player.createNode("<image id='videoselected"+str(index)+
                "' href='images/VideoSelected.png'/>")
        node.y = 43
        node.width = VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2
        node.height = VIDEO_THUMBNAIL_HEIGHT+BORDER_WIDTH*2
        node.opacity = 0
        videoDiv.addChild(node)
        
        node = Player.createNode("<video id='video"+str(index)+"' href='"+href+
                "' loop='true' onmouseover='videoMouseOver' onmouseout='videoMouseOut' onmouseup='videoMouseUp'/>")
        node.x = BORDER_WIDTH
        node.y = 43+BORDER_WIDTH
        node.height = VIDEO_THUMBNAIL_HEIGHT
        node.width = VIDEO_THUMBNAIL_WIDTH
        videoDiv.addChild(node)

        node = Player.createNode("<words/>")
        node.x = 22
        node.y = 6 
        node.size = 30
        node.font = "EurostileCondensed" 
        node.color = "F39C01"
        node.text = title
        videoDiv.addChild(node)
        
    curEntry = 0
    for videoInfo in curVideoInfos:
#        href = VIDEO_DIR+"thumbs/"+videoInfo.videoFile
        href = VIDEO_DIR+ourDirInfos[curDir].dirName+"/"+videoInfo.videoFile
        createVideoNode(curEntry, href, videoInfo.title)
        curEntry += 1
#    files = os.listdir(VIDEO_DIR+"thumbs/")
#    numVideos = len(files)
#    curEntry = 0
#    for i in range(numVideos):
#        videoName = VIDEO_DIR+"thumbs/"+files[i]
#        print videoName
#        if not(stat.S_ISDIR(os.stat(videoName).st_mode)):
#            createVideoNode(curEntry, videoName)
#            curEntry+=1

def removeVideoNodes():
    VideoArea = Player.getElementByID("videos")
    for i in range(0, VideoArea.getNumChildren()):
        VideoArea.removeChild(0)

def startVideos():
    VideoArea = Player.getElementByID("videos")
    for i in range(0, VideoArea.getNumChildren()):
        CurVideoArea = VideoArea.getChild(i)
        CurVideo = CurVideoArea.getChild(2)
        videoPos = (VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2)*i-sb.getPos()
        if videoPos > -VIDEO_THUMBNAIL_WIDTH and videoPos < 1854:
            CurVideo.play()
        else:
            CurVideo.pause()

def selectVideo(selectedVideo):
    global ourSelectedVideo
    global curVideoInfos
    print "selectVideo"
    if ourSelectedVideo != selectedVideo:
        if ourSelectedVideo != -1:
            Player.getElementByID("videoselected"+str(ourSelectedVideo)).opacity=0.0
            Player.getElementByID("videounselected"+str(ourSelectedVideo)).opacity=0.67
        ourSelectedVideo = selectedVideo
        Player.getElementByID("videoselected"+str(ourSelectedVideo)).opacity=0.67
        Player.getElementByID("videounselected"+str(ourSelectedVideo)).opacity=0.0
        mainVideo = Player.getElementByID("mainvideo")
        smallVideo = Player.getElementByID("video"+str(ourSelectedVideo))
        mainVideo.href=VIDEO_DIR+ourDirInfos[curDir].dirName+"/"+curVideoInfos[ourSelectedVideo].videoFile
        mainVideo.play()
        mainVideo.seekToFrame(smallVideo.getCurFrame())
        videoInfo = curVideoInfos[ourSelectedVideo]
        Player.getElementByID("infotitle").text=videoInfo.title
        Player.getElementByID("infotext").text=videoInfo.description
        if videoInfo.imageFile1 != "":
            Player.getElementByID("infoimage1").href="images/storyboard/"+videoInfo.imageFile1
        else:
            Player.getElementByID("infoimage1").href=""
        if videoInfo.imageFile2 != "":
            Player.getElementByID("infoimage2").href="images/storyboard/"+videoInfo.imageFile2
        else:
            Player.getElementByID("infoimage2").href=""

def selectDir(index):
    global curDir
    global curVideoInfos
    global sb
    global ourSelectedVideo
    print "selectDir"+str(index)
    if curDir != index:
        if curDir != -1:
            removeVideoNodes()
        curDir = index
        curVideoInfos = ourDirInfos[curDir].videoInfos
        initVideoNodes()
        sb.setRange(getVideoViewportWidth())
        sb.setSlider(0, VIDEO_AREA_WIDTH)
        ourSelectedVideo = -1
        mainVideo = Player.getElementByID("mainvideo")
        mainVideo.href = ""


def selectcwars():
    selectDir(0)
    Player.getElementByID("dir1bkgnd").href="images/DirSelected.png"
    Player.getElementByID("dir2bkgnd").href="images/Dir.png"

def selectchill():
    global Player
    selectDir(1)
    Player.getElementByID("dir1bkgnd").href="images/Dir.png"
    Player.getElementByID("dir2bkgnd").href="images/DirSelected.png"

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

def getVideoViewportWidth():
    global curVideoInfos
    return len(curVideoInfos)*(VIDEO_THUMBNAIL_WIDTH+BORDER_WIDTH*2)

Player = avg.Player()
Log = avg.Logger.get()
bDebug = not(os.getenv('AVG_DEPLOY'))
if (bDebug):
    Player.setResolution(0, 0, 550, 0) 
else:
    Player.setResolution(1, 0, 0, 0)
    Log.setFileDest("/var/log/cleuse.log")
Log.setCategories(Log.APP |
                  Log.WARNING | 
                  Log.PROFILE |
#                 Log.PROFILE_LATEFRAMES |
                  Log.CONFIG
#                 Log.MEMORY  |
#                 Log.BLTS    
#                  Log.EVENTS |
#                  Log.EVENTS2
                  )
Player.loadFile("videochooser2.avg")
anim.init(Player)
Player.setVBlankFramerate(2)
sb = ScrollBar(Player, Player.getElementByID("videoarea"), 6, 398, 
        VIDEO_AREA_WIDTH, 1000)
Player.setInterval(10, onFrame)
Player.play()
