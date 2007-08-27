
from libavg import avg

global numScrollBars
numScrollBars=0
global ourPlayer

class ScrollBar:
    def __init__(self, player, parentNode, x, y, width, sliderRange):
        global numScrollBars
        global ourPlayer
        self.__parentNode = parentNode
        ourPlayer = player
        self.__node = player.createNode("<div/>")
        self.__node.x = x
        self.__node.y = y
        self.__node.width = width
        self.__node.height = 50
        self.__width = width
        self.__sliderPos = 0
        self.__sliderWidth = 100
        self.__sliderRange = sliderRange
        self.__endWidth = 5
        self.__scrollerEndWidth = 7
        parentNode.appendChild(self.__node)
        
        node = player.createNode("<image href='images/Scrollbar.png' x='1' y='0'/>")
        node.id = "scrollerbg"+str(numScrollBars)
        node.width=width-2
        node.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.ScrollbarMouseDown);
        node.setEventHandler(avg.CURSORDOWN, avg.TOUCH, self.ScrollbarMouseDown);
        node.setEventHandler(avg.CURSORUP, avg.MOUSE, self.ScrollerMouseUp);
        node.setEventHandler(avg.CURSORUP, avg.TOUCH, self.ScrollerMouseUp);
        node.setEventHandler(avg.CURSORMOTION, avg.MOUSE, self.ScrollerMouseMove);
        node.setEventHandler(avg.CURSORMOTION, avg.TOUCH, self.ScrollerMouseMove);
        node.setEventHandler(avg.CURSOROUT, avg.MOUSE, self.ScrollerMouseOut);
        node.setEventHandler(avg.CURSOROUT, avg.TOUCH, self.ScrollerMouseOut);

        self.__node.appendChild(node)
        
        node = player.createNode("<image href='images/ScrollbarBegin.png' x='0' y='0'/>")
        self.__node.appendChild(node)
        
        node = player.createNode("<image href='images/ScrollbarEnd.png' y='0'/>")
        node.x = width-self.__endWidth
        self.__node.appendChild(node)
        
        self.__sliderStartNode = player.createNode(
                "<image href='images/ScrollbarScrollerBegin.png'/>")
        self.__node.appendChild(self.__sliderStartNode)
        self.__sliderNode = player.createNode(
                "<image href='images/ScrollbarScroller.png'/>")
        self.__sliderNode.id = "scroller"+str(numScrollBars)
        self.__sliderNode.setEventHandler(avg.CURSORUP, avg.MOUSE, self.ScrollerMouseUp);
        self.__sliderNode.setEventHandler(avg.CURSORUP, avg.TOUCH, self.ScrollerMouseUp);
        self.__sliderNode.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.ScrollerMouseDown);
        self.__sliderNode.setEventHandler(avg.CURSORDOWN, avg.TOUCH, self.ScrollerMouseDown);
        self.__sliderNode.setEventHandler(avg.CURSORMOTION, avg.MOUSE, self.ScrollerMouseMove);
        self.__sliderNode.setEventHandler(avg.CURSORMOTION, avg.TOUCH, self.ScrollerMouseMove);
        self.__node.appendChild(self.__sliderNode)
        
        self.__sliderEndNode = player.createNode(
                "<image href='images/ScrollbarScrollerEnd.png'/>")
        self.__node.appendChild(self.__sliderEndNode)
        
        self.__startCallback = None
        self.__moveCallback = None
        self.__stopCallback = None
        self.__startScrollCursor = 0
        self.__startScrollPos = 0
        self.CurCursor = None
        self.__positionSlider()
        numScrollBars+=1
    def ScrollerMouseUp(self, Event): 
        if self.CurCursor == Event.cursorid:
            self.CurCursor = None
            self.onMoveStop()
            Event.node.releaseEventCapture(Event.cursorid)
    def ScrollerMouseMove(self, Event):
        if self.CurCursor == Event.cursorid:
            pixelsMoved = Event.x-self.__startScrollCursor
            sbMoved = float(pixelsMoved)/(self.__width-1)*self.__sliderRange
            newPos = self.__startScrollPos+sbMoved
            self.moveTo(newPos)
    def ScrollbarMouseDown(self, Event):
        if (self.CurCursor is not None) and self.CurCursor != Event.cursorid:
            return
        absPos = (Event.x, Event.y)
        relPos = Event.node.getRelPos(absPos)[0]/self.__width
        self.__sliderPos = relPos*self.__sliderRange -self.__sliderWidth/2
        if self.__sliderPos < 0:
            self.__sliderPos = 0
        if self.__sliderPos > self.__sliderRange-self.__sliderWidth:
            self.__sliderPos = self.__sliderRange-self.__sliderWidth
        self.__positionSlider()
        self.CurCursor = Event.cursorid
        self.__startScrollCursor = Event.x
        self.__startScrollPos = self.__sliderPos
        Event.node.setEventCapture(Event.cursorid)
        self.onMoveStart()
    def ScrollerMouseDown(self, Event):
        if (self.CurCursor is not None) and self.CurCursor != Event.cursorid:
            return
        self.CurCursor = Event.cursorid
        self.__startScrollCursor = Event.x
        self.__startScrollPos = self.__sliderPos
        Event.node.setEventCapture(Event.cursorid)
        self.onMoveStart()
    def ScrollerMouseOut(self, Event):
        if self.CurCursor == Event.cursorid:
            print ("out?!")        

    def setRange(self, range):
        self.__sliderRange = range
        self.__positionSlider()

    def setSlider(self, pos, width):
        self.__sliderPos = pos
        self.__sliderWidth = width
        widthInPixels = int((float(self.__sliderWidth)/self.__sliderRange)*self.__width)
        if widthInPixels < 40:
            self.__sliderWidth = (self.__sliderRange*40)/self.__width
        self.__positionSlider()

    def setCallbacks(self, startCallback, moveCallback, stopCallback):
        self.__startCallback = startCallback
        self.__moveCallback = moveCallback
        self.__stopCallback = stopCallback

    def getPos(self):
        return self.__sliderPos

    def moveTo(self, pos):
        self.__sliderPos = pos
        if self.__sliderPos > self.__sliderRange-self.__sliderWidth:
            self.__sliderPos = self.__sliderRange-self.__sliderWidth
        if self.__sliderPos < 0:
            self.__sliderPos = 0
        self.__positionSlider()
        if self.__moveCallback != None:
            self.__moveCallback(self.__sliderPos)

    def onMoveStart(self):
        if self.__startCallback != None:
            self.__startCallback(self.__sliderPos)
    
    def onMoveStop(self):
        if self.__stopCallback != None:
            self.__stopCallback()

    def __positionSlider(self):
        relativePos = float(self.__sliderPos)/self.__sliderRange
        startPos = int(relativePos*(self.__width-1))
        self.__sliderStartNode.x = startPos+1
        self.__sliderNode.x = startPos+2
        width = int((float(self.__sliderWidth)/self.__sliderRange)*self.__width)
        self.__sliderNode.width = width-2
        self.__sliderNode.height = 50
        self.__sliderEndNode.x = startPos+width

