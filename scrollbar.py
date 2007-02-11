
global numScrollBars
numScrollBars=0
global scrollBarRegistry
scrollBarRegistry={}
global ourPlayer

def ScrollerMouseDown():
    Event = ourPlayer.getCurEvent()
    scrollBar = scrollBarRegistry[Event.node.id]
    scrollBar.ScrollerMouseDown(Event)

def ScrollerMouseMove():
    Event = ourPlayer.getCurEvent()
    scrollBar = scrollBarRegistry[Event.node.id]
    scrollBar.ScrollerMouseMove(Event)
def ScrollerMouseUp():
    Event = ourPlayer.getCurEvent()
    scrollBar = scrollBarRegistry[Event.node.id]
    scrollBar.ScrollerMouseUp(Event)

def ScrollerMouseOut():
    Event = ourPlayer.getCurEvent()
    scrollBar = scrollBarRegistry[Event.node.id]
    scrollBar.ScrollerMouseOut(Event)

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
        parentNode.addChild(self.__node)
        
        node = player.createNode("<image href='images/Scrollbar.png' x='0' y='0' "
                "onmouseup='ScrollerMouseUp' onmousemove='ScrollerMouseMove' "
                "onmouseout='ScrollerMouseOut' "
                "ontouchup='ScrollerMouseUp' ontouchmove='ScrollerMouseMove' "
                "/>")
        node.id = "scrollerbg"+str(numScrollBars)
        node.x = 1 
        node.width=width-2
        scrollBarRegistry[node.id] = self
        self.__node.addChild(node)
        
        node = player.createNode("<image href='images/ScrollbarBegin.png' x='0' y='0'/>")
        self.__node.addChild(node)
        
        node = player.createNode("<image href='images/ScrollbarEnd.png' y='0'/>")
        node.x = width-self.__endWidth
        self.__node.addChild(node)
        
        self.__sliderStartNode = player.createNode(
                "<image href='images/ScrollbarScrollerBegin.png'/>")
        self.__node.addChild(self.__sliderStartNode)
        self.__sliderNode = player.createNode(
                "<image href='images/ScrollbarScroller.png' "
                "onmousedown='ScrollerMouseDown' onmouseup='ScrollerMouseUp' "
                "onmousemove='ScrollerMouseMove' "
                "ontouchdown='ScrollerMouseDown' ontouchup='ScrollerMouseUp' "
                "ontouchmove='ScrollerMouseMove' "
                "/>")
        self.__sliderNode.id = "scroller"+str(numScrollBars)
        self.__node.addChild(self.__sliderNode)
        
        self.__sliderEndNode = player.createNode(
                "<image href='images/ScrollbarScrollerEnd.png'/>")
        self.__node.addChild(self.__sliderEndNode)
        
        self.__startCallback = None
        self.__moveCallback = None
        self.__stopCallback = None
        self.__startScrollCursor = 0
        self.__startScrollPos = 0
        self.CurCursor = None
        self.__positionSlider()
        numScrollBars+=1
        scrollBarRegistry[self.__sliderNode.id] = self
    def ScrollerMouseUp(self, event):
        if self.CurCursor == event.cursorid:
            self.CurCursor = None
            self.onMoveStop()
            event.node.releaseEventCapture(event.cursorid)
    def ScrollerMouseMove(self, event):
        if self.CurCursor == event.cursorid:
            pixelsMoved = event.x-self.__startScrollCursor
            sbMoved = float(pixelsMoved)/(self.__width-1)*self.__sliderRange
            newPos = self.__startScrollPos+sbMoved
            self.moveTo(newPos)
    def ScrollerMouseDown(self, event):
        if (self.CurCursor is not None) and self.CurCursor != event.cursorid:
            return
        self.CurCursor = event.cursorid
        self.__startScrollCursor = event.x
        self.__startScrollPos = self.__sliderPos
        event.node.setEventCapture(event.cursorid)
        self.onMoveStart()
    def ScrollerMouseOut(self, event):
        if self.CurCursor == event.cursorid:
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
            self.__startCallback()
    
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

