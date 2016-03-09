from display.sprite import Sprite;
from display.drawer import Drawer;
import random;

class Game:
    def __init__(self, width, height):
        self._width = width;
        self._height = height;
        
        self._initDrawer_();
        self._initPlayer_();
        self._initGround_();
        self._initBackground_();
        self._rad = 0;
        self._player.x = width/2 - 5;
        self._jumping = False;
        self._vy = 0;
        self._g = 0.25;
        self._over = False;
    #ドロワァ初期化
    def _initDrawer_(self):
        self._drawer = Drawer();
        self._drawer.setClearChar(" ");
        self._drawer.setSize(self._width, self._height);
    #プレイヤー初期化
    def _initPlayer_(self):
        self._player = Player();
    #地面初期化
    def _initGround_(self):
        self._ground = Ground(self._width, self._height);
    #背景初期化
    def _initBackground_(self):
        self._background = Background(self._width, self._height/4);
    #レンダリング
    def _render_(self):
        #クリア
        self._drawer.clear();
        #背景
        self._background.renderToDrawer(self._drawer);
        #地面を描く
        self._ground.renderToDrawer(self._drawer);
        #プレイヤーを描く
        self._player.renderToDrawer(self._drawer);
        #枠を描く
        self._drawBorder_();
        #画面更新
        self._drawer.render();
    def _drawBorder_(self):
        for x in range(self._width):
            self._drawer.addDot(x, 0, "=");
            self._drawer.addDot(x, self._height-1, "=");
        for y in range(self._height):
            self._drawer.addDot(0, y, "|");
            self._drawer.addDot(self._width-1, y, "|");
    #ゲーム更新
    def tick(self):
        if self._over : return;
        self._vy += self._g;
        #地形更新
        self._ground.tick();
        #プレイヤー更新        
        self._player.followBodies();
        #プレイヤーのY更新
        groundY = self._ground.getGround(self._player.x+2)-2;
        self._player.y += self._vy;
        if self._vy > 0 and self._player.y >= groundY:
            self._player.y = groundY;
            #着地したらジャンプ解除
            self._jumping = False;
        if self._ground.isInToge(self._player.x+2, self._player.y) and self._jumping == False:
            self.over();
        #レンダリング
        self._render_();
    #ゲームオーバー
    def over(self):
        self._over = True;
    #ジャンプ
    def jump(self):
        #二段ジャンプ禁止
        if self._jumping: return;
        self._vy = -2;
        self._jumping = True
    #キーボード
    def keyboard(self, key):
        if key==" ":
            self.jump();
class Ground():
    def __init__(self, width, height):
        self._groundsY = [];
        self._width = int(width);
        self._height = int(height);
        self._groundLength = int(width);
        self._headY = 10;
        self._vy = 0;
        self._tick = 0;
        self._generateToge_(1);
        for n in range(self._groundLength):
            self._groundsY.append(self._headY);n;
    #更新
    def tick(self):
        self._tick -= 1;
        prevHeadY = self._headY;
        self._headY += self._vy;
        if self._tick < 0 or self._headY < 8 or self._headY > self._height - 4:
            self._tick = random.randint(10, 120);
            self._vy = random.uniform(-0.4, 0.4);
            self._headY = prevHeadY;
        self._groundsY[0] = int(self._headY);
        for n in range(1, self._groundLength):
            i = self._groundLength - n;
            self._groundsY[i] += (self._groundsY[i - 1] - self._groundsY[i])*1;
        for toge in self._toges:
            toge.x += 1;
            if toge.x == -5:
                toge.y = self.getGround(0) - 4;
            if(toge.x > self._width):
                toge.x = - random.randint(20, 80);
    #ドロワァへ描画
    def renderToDrawer(self, drawer):
        for toge in self._toges:
            drawer.renderSprite(toge);
        x = 0;
        prevY = -1;
        for ty in self._groundsY:
            if prevY > ty:
                drawer.addDot(x, ty, "w");
            elif prevY < ty:
                drawer.addDot(x-1, prevY, "w");
                drawer.addDot(x, ty, "W");
            else:
                drawer.addDot(x, ty, "W");
            prevY = ty;
            for gy in range(ty+1, self._height):
                drawer.addDot(x, gy, ".");
                gy;
            x += 1;
    #地面の高さを知りたい
    def getGround(self, x):
        if x < 0 :
            return self._groundsY[0];
        elif x >= self._width:
            return self._groundsY[self._width-1];
        return self._groundsY[int(x)];
    #トゲ生成
    def _generateToge_(self, num):
        self._toges = [];
        for n in range(num):
            toge = Sprite([' ',' ',' ',' ','/','\\',' ',' ',' ',' ',
                           ' ',' ',' ','/',' ',' ','\\',' ',' ',' ',
                           ' ',' ','/',' ',' ',' ',' ','\\',' ',' ',
                           ' ','/',' ',' ',' ',' ',' ',' ','\\',' ',
                           '/',' ',' ',' ',' ',' ',' ',' ',' ','\\'],10,5);
            toge.y = self._height;
            self._toges.append(toge);n;
    #とげに当たるか
    def isInToge(self, x, y):
        for toge in self._toges:
            if x > toge.x and y > toge.y and x < toge.x + toge.getWidth() and y < toge.y + toge.getHeight():
                return True;
        return False;
class Player():
    def __init__(self):
        self._initBody_(13);
        self._x = 0;
        self._y = 0;
    #体初期化
    def _initBody_(self, length):
        self._bodyLength = length;
        #顔
        self._face = Sprite(
        ['(','^','o','^',')'],
        5,1
        );
        #体
        self._bodies = [];
        for n in range(length):
            #体
            texture = ['(',' ',' ',' ',')'];
            #偶数の時だけ足をはやす
            if n%2==0 : texture += ['J',' ',' ',' ','L'];
            body = Sprite(texture, 5, 1);
            self._bodies.append(body);
    #ドロワァへ描画
    def renderToDrawer(self, drawer):
        for body in reversed(self._bodies):
            drawer.renderSprite(body);
        drawer.renderSprite(self._face);
    #体が頭を追尾
    def followBodies(self):
        self._bodies[0].y = self._face.y;
        for n in range(1, self._bodyLength):
            i = self._bodyLength - n;
            self._bodies[i].y += (self._bodies[i - 1].y - self._bodies[i].y)*1;
    #ゲッターセッタープロパティとか
    def getX(self):
        return self._x;
    def setX(self, val):
        self._x = val;
        self._face.x = val;
        for body in self._bodies:
            val+=1;
            body.x = val;
    def getY(self):
        return self._y;
    def setY(self, val):
        self._y = val;
        self._face.y = val;
    x = property(getX, setX);
    y = property(getY, setY);
    
class Background():
    def __init__(self, width ,height):
        self._clouds = [];
        self._width = width;
        self._height = height;
        self._initClouds_(3);
    #雲生成
    def _initClouds_(self, num):
        for n in range(num):
            cloud = Sprite([ 
                            ' ','_','_','_','_','_','_','_',' ',
                            '/',' ',' ',' ',' ',' ',' ',' ','\\',
                           '\\','_','_','_','_','_','_','_','/'],
                           9, 3);
            self._clouds.append(cloud);
            cloud.y = random.randint(0, self._height);
            cloud.x = -random.randint(9, 80);n
    #雲描画
    def renderToDrawer(self, drawer):
        for cloud in self._clouds:
            cloud.x+=1;
            drawer.renderSprite(cloud);
            if cloud.x > self._width:
                cloud.y = random.randint(0, self._height);
                cloud.x = -random.randint(9, 80);
                