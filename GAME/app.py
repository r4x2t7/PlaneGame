# -*- Coding: utf-8 -*-
# @Time    : 2020/12/10 14:59
# @Author  : 周昊
# @FileName: app.py
# @Software: PyCharm
# @Github :  https://github.com/r4x2t7/jw
# @Exercises:
import os
import random
import math
import pygame
import sys
import time
from tkinter import *
from tkinter import messagebox
PLANEIMG = "images/wsparticle_test_001.png"
BULLET = "images/img_bullet.png"
PLANESIZE = 90  # 飞机对象直径（近似圆形）
SMALLSIZE = 100
count = 0
def start():
    FPS=60 # 游戏帧率
    WINWIDTH = 512  # 窗口宽度
    WINHEIGHT = 768  # 窗口高度
    MOVESTEP=5  # 移动速度

    pygame.init() # pygame初始化，必须有，且必须在开头
    pygame.mixer.init()
    pygame.mixer.music.load("audio/背景音乐.mp3")
    pygame.mixer.music.play(-1)
    sound = pygame.mixer.Sound("audio/爆炸.ogg")
    # 创建主窗体
    clock=pygame.time.Clock() # 用于控制循环刷新频率的对象
    win=pygame.display.set_mode((WINWIDTH,WINHEIGHT))
    background = pygame.image.load("images/img_bg_level_1.jpg")

    plane=Plane(win,200,600)
    hm=HuajiManager(win)
    mx,my=0,0 # 记录移动方向
    def paused():
        pausedmenu= Toplevel()
        def destory():
            pausedmenu.destroy()
        imgjixu=PhotoImage(file="images/jixuyouxi.png")
        labeltext=Label(pausedmenu,text="游戏暂停")
        labeltext.pack()
        pausedmenu.overrideredirect(True)
        width,height=300,100
        screenwidth=pausedmenu.winfo_screenwidth()
        screenheight=pausedmenu.winfo_screenheight()
        alighstr='%dx%d+%d+%d'%(width,height,(screenwidth-width)/2,(screenheight/2))
        pausedmenu.geometry(alighstr)
        buttonpause=Button(pausedmenu,image=imgjixu,command=destory)
        buttonpause.pack()
        pausedmenu.title("暂停/继续")
        pausedmenu.resizable(width=False,height=False)
        pausedmenu.mainloop()
    while True:
        win.blit(background,(0,0))
        # plane.check_crash(hm.score1)
        # score=hm.score1*10
        # score=bullet.check_hit(count)*10

        scorefont=pygame.font.SysFont("华文彩云",30)
        text_surface=scorefont.render(u"分数：%s"%str(count),True,(255,255,255))
        win.blit(text_surface,(10,20))

        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LEFT or event.key == ord('a'):
                    mx=-1
                if event.key==pygame.K_RIGHT or event.key == ord('d'):
                    mx=1
                if event.key==pygame.K_UP  or event.key == ord('w'):
                    my=-1
                if event.key==pygame.K_DOWN  or event.key == ord('s'):
                    my=1
                if event.key == pygame.K_ESCAPE:
                    paused()

            if event.type == pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key == ord('a'):
                    if mx==-1:
                        mx=0
                if event.key==pygame.K_RIGHT or event.key == ord('d'):
                    if mx==1:
                        mx=0
                if event.key==pygame.K_UP  or event.key == ord('w'):
                    if my==-1:
                        my=0
                if event.key==pygame.K_DOWN  or event.key == ord('s'):
                    if my==1:
                        my=0
                # if event.key == pygame.K_ESC or event.key == ord('^['):


        plane.check_all_hit(hm.huajilist)
        plane.check_crash(hm.huajilist)
        if plane.lives<=0:
            Tk().wm_withdraw()
            messagebox.showwarning("你死了",message="正在写入分数请等待。。。")
            with open(file='rank/rank.txt', mode='a')as f:
                f.write(str(count)+'\n')
            time.sleep(1)
            pygame.quit()

        hm.generate()
        hm.update()
        hm.draw()

        plane.move(mx*MOVESTEP,my*MOVESTEP)
        plane.draw()

        plane.fire()
        plane.update_bullets()
        plane.draw_bullets()

        clock.tick(FPS) # 控制循环刷新频率,每秒刷新FPS对应的值的次数
        pygame.display.update()



# 敌机 - 滑稽
class Huaji():
    imgpath = "images/img_plane_enemy (2).png"
    speed = 2

    def __init__(self, master, x, y=0):
        self._master = master  # 父控件
        self.image = pygame.image.load(self.imgpath)
        self.x = x
        self.y = y
        self.lives = 1

    # 移动敌机，更新敌机位置
    def update(self):
        self.y += self.speed

    def draw(self):
        self._master.blit(self.image, (self.x, self.y))

    def inWindow(self):
        if self.y < 0 or self.y > self._master.get_height():
            return False
        return True

    def get_center_XY(self):
        # 获取圆心坐标
        return (self.x + SMALLSIZE / 2, self.y + SMALLSIZE / 2)

    def get_radius(self):
        # 获取半径
        return SMALLSIZE / 2


class HuajiManager():
    cd = 35  # 生成滑稽的时间间隔

    def __init__(self, master):
        self._master = master
        self.t = 0
        self.huajilist = []

    def generate(self):
        self.t += 1
        if self.t % self.cd == 0:
            x = random.randint(0, self._master.get_width() - SMALLSIZE)
            ji = Huaji(self._master, x, 0)
            self.huajilist.append(ji)

    def update(self):
        survive = []
        for huaji in self.huajilist:
            huaji.update()
            if huaji.inWindow() and huaji.lives > 0:
                survive.append(huaji)
        self.huajilist = survive

    def draw(self):
        for huaji in self.huajilist:
            huaji.draw()





class Plane():
    firedelay = 15  # 发射子弹时间间隔

    def __init__(self, master, x, y, img_path=PLANEIMG, img_path_bullets=BULLET):
        self._master = master  # 父控件
        self.image = pygame.image.load(img_path)  # 飞机图像
        self.image1 = pygame.image.load(img_path_bullets)
        # 飞机位置-坐标
        self.x = x
        self.y = y
        self.lives = 3
        self.t = 0
        self.bullets = []  # 发射的子弹

    # 移动飞机
    def move(self, x, y):
        if 0 <= self.x + PLANESIZE / 2 + x <= self._master.get_width():
            self.x += x
        if 0 <= self.y + PLANESIZE / 2 + y <= self._master.get_height():
            self.y += y

    # 绘制飞机
    def draw(self):
        self._master.blit(self.image, (self.x, self.y))

    # 发射子弹
    def fire(self):
        self.t += 1
        if self.t >= self.firedelay:
            self.t = 0
            # 子弹初始坐标
            bx = self.x + int(self.image.get_width() / 2)
            by = self.y
            bullet = Bullet(self._master, bx, by)
            self.bullets.append(bullet)

    # 更新子弹位置，清除失效的子弹
    def update_bullets(self):
        survive = []
        for b in self.bullets:
            b.update()
            if b.on:
                survive.append(b)
        self.bullets = survive

    # 绘制子弹
    def draw_bullets(self):
        for b in self.bullets:
            b.draw()

    def check_all_hit(self, huajilist):
        survive = []
        for b in self.bullets:
            b.check_hit(huajilist)
            if b.on:
                survive.append(b)
        self.bullets = survive

    def get_distance(self, xy):
        x, y = xy
        cx = self.x + PLANESIZE / 2
        cy = self.y + PLANESIZE / 2
        return math.sqrt(math.pow(cx - x, 2) + math.pow(cy - y, 2))

    def check_crash(self, huajilist):
        for huaji in huajilist:
            if huaji.lives > 0 and huaji.inWindow():
                d = self.get_distance(huaji.get_center_XY())
                if d <= PLANESIZE / 2 + huaji.get_radius():
                    # hit
                    self.lives -= 1
                    huaji.lives -= 1


class Bullet():
    speed = 2  # 速度
    color = (255, 0, 0)  # 颜色
    radius = 10  # 半径

    def __init__(self, master, x, y, ):
        self._master = master  # 父控件
        self.x = x
        self.y = y
        self.on = True  # 记录子弹状态，初始为True，子弹失效（超出边界或者碰到敌机）时为False

    # 更新子弹位置，移动子弹
    def update(self):
        self.y -= self.speed

        if self.y <= 0:
            self.on = False

    # 绘制飞机
    def draw(self):
        pygame.draw.circle(self._master, self.color, (self.x, self.y), self.radius, 2)

    def get_distance(self, xy):
        x, y = xy
        return math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2))

    def check_hit(self, huajilist, ):
        global count
        if not self.on:
            return
        for huaji in huajilist:
            if huaji.lives > 0 and huaji.inWindow():
                d = self.get_distance(huaji.get_center_XY())
                if d <= huaji.get_radius():
                    # hit
                    self.on = False
                    huaji.lives -= 1
                    count += 100
                    self.count1 = count
                    print(self.count1)
