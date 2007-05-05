
global numScrollBars
numScrollBars=0
global scrollBarRegistry
scrollBarRegistry={}
global ourPlayer
global ourLastScrollPos
global ourIsScrolling
ourIsScrolling=False

def ScrollerMouseDown():
    global ourLastScrollPos
    global ourIsScrolling
    ourIsScrolling = True
    Event = ourPlayer.getCurEvent()
    ourLastScrollPos = Event.x
    Event.node.setEventCapture()
    scrollBar = scrollBarRegistry[Event.node.id]
    scrollBar.onMoveStart()

def ScrollerMouseMove():
    global ourLastScrollPos
    global ourIsScrolling
    if ourIsScrolling:
        Event = ourPlayer.getCurEvent()
        scrollBar = scrollBarRegistry[Event.node.id]
        scrollBar.move(Event.x-ourLastScrollPos)
        ourLastScrollPos = Event.x

def ScrollerMouseUp():
    global ourIsScrolling
    if ourIsScrolling:
        ourIsScrolling = False
        Event = ourPlayer.getCurEvent()
        scrollBar = scrollBarRegistry[Event.node.id]
        scrollBar.onMoveStop()
        Event.node.releaseEventCapture()

def ScrollerMouseOut():
    global ourIsScrolling
    if ourIsScrolling:
        print ("out?!")        

class ScrollBar:
    def __init__(self, player, parentNode, x, y, width, sliderRange):
        global numScrollBars
        global ourPlayer
        self.__parentNode = parentNode
        ourPlayer = player
        self.__node = player.createNode("<div/>")
        self.__node.x = x
        self.__node.y = y
        self.__width = width
        self.__sliderPos = 0
        self.__sliderWidth = 100
        self.__sliderRange = sliderRange
        parentNode.addChild(self.__node)
        
        node = player.createNode("<image href='images/ScrollbarEnd.png' x='0' y='0'/>")
        self.__node.addChild(node)
        
        node = player.createNode("<image href='images/Scrollbar.png' x='1' y='0' oncursorup='ScrollerMouseUp' oncursormove='ScrollerMouseMove' oncursorout='ScrollerMouseOut'/>")
        node.id = "scrollerbg"+str(numScrollBars)
        node.width=width-2
        node.height=50
        scrollBarRegistry[node.id] = self
        self.__node.addChild(node)
        
        node = player.createNode("<image href='images/ScrollbarEnd.png' y='0'/>")
        node.x = width-1
        self.__node.addChild(node)
        
        self.__sliderStartNode = player.createNode(
                "<image href='images/ScrollbarScrollerEnd.png'/>")
        self.__node.addChild(self.__sliderStartNode)
        self.__sliderNode = player.createNode(
                "<image href='images/ScrollbarScroller.png' oncursordown='ScrollerMouseDown' oncursorup='ScrollerMouseUp' oncursormove='ScrollerMouseMove'/>")
        self.__sliderNode.id = "scroller"+str(numScrollBars)
        self.__node.addChild(self.__sliderNode)
        
        self.__sliderEndNode = player.createNode(
                "<image href='images/ScrollbarScrollerEnd.png'/>")
        self.__node.addChild(self.__sliderEndNode)
        
        self.__startCallback = None
        self.__moveCallback = None
        self.__stopCallback = None
        self.__positionSlider()
        numScrollBars+=1
        scrollBarRegistry[self.__sliderNode.id] = self

    def setRange(self, range):
        self.__sliderRange = range
        self.__positionSlider()

    def setSlider(self, pos, width):
        self.__sliderPos = pos
        self.__sliderWidth = width
        self.__positionSlider()

    def setCallbacks(self, startCallback, moveCallback, stopCallback):
        self.__startCallback = startCallback
        self.__moveCallback = moveCallback
        self.__stopCallback = stopCallback

    def getPos(self):
        return self.__sliderPos

    def move(self, offset):
        # Offset is in pixels
        realOffset = float(offset)/(self.__width-1)*self.__sliderRange
        self.__sliderPos += realOffset
        if self.__sliderPos > self.__sliderRange-self.__sliderWidth:
            self.__sliderPos = self.__sliderRange-self.__sliderWidth
        if self.__sliderPos < 0:
            self.__sliderPos = 0
        if self.__positionSlider != None:
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

