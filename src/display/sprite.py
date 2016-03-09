class Sprite:
    def __init__(self, body=["@"], width=1, height=1):
        self._body = body;
        self._width = width;
        self._height = height;
        self._x = 0.0;
        self._y = 0.0;
        
    def _setX(self, val):
        self._x = val;
    def _setY(self, val):
        self._y = val;
    def setBody(self, val):
        self._body = val;
    def setWidth(self, val):
        self._width = val;
    def setHeight(self, val):
        self._height = val;
    
    
    def _getX(self):
        return self._x;
    def _getY(self):
        return self._y;
    def getWidth(self):
        return self._width;
    def getHeight(self):
        return self._height;
    def getBody(self):
        return self._body;
    
    x = property(_getX, _setX);
    y = property(_getY, _setY);