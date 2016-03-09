from game.game import Game;
import math;
import threading;
import msvcrt;
import sys, os;
g = Game(60, 20);

def loop():
    g.tick();
    t = threading.Timer(1/200, loop);
    t.start();
loop();

#キーボード
while True:
    val = msvcrt.getch().decode("utf-8");
    if val == "q":
        os.system("clear");
        print("exit");
        os._exit(0);
        break;
    g.keyboard(val);