import os;
class Drawer:
    def __init__(self):
        #大きさ
        self._width = 0;
        self._height = 0;
        #背景
        self._clearChar = "#";
        self._stage = [];
        self._sprites = [];
        self._stageLength = 0;
    #大きさ設定
    def setSize(self, width, height):
        self._width = int(width);
        self._height = int(height);
        self._stageLength = width * height + height;
    #背景色
    def setClearChar(self, char):
        self._clearChar = char;
    #クリア
    def clear(self):
        self._stage = [];
        for h in range(self._height):
            for w in range(self._width):
                self._stage.append(self._clearChar);
                h;w;
            self._stage.append("\n");
    #レンダリング
    def render(self):
        os.system("clear");
        print(''.join(self._stage));
    #ドット描画
    def addDot(self, x, y, char):
        #intにする
        x = int(x);
        y = int(y);
        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return;
        i = y * self._width + x + y;
        self._stage[i] = char;
    #スプライト描画
    def renderSprite(self, sprite):
        bx = sprite.x;
        by = sprite.y;
        body = sprite.getBody();
        i = 0;
        for char in body:
            y = int(i / sprite.getWidth());
            x = i - y * sprite.getWidth();
            self.addDot(x + bx, y + by, char);
            i += 1;