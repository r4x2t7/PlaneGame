# -*- Coding: utf-8 -*-
# @Time    : 2020/11/28 14:59
# @Author  : 周昊
# @FileName: miangui.py
# @Software: PyCharm
# @Github :  https://github.com/r4x2t7/jw
# @Exercises:
from tkinter import *
import sys
from tkinter.messagebox import *
import time
import pygame
from GAME.app import start
from GAME2.app import start2
import os
pygame.init()
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        # 判断当前事件是否为点击右上角退出键
        pygame.quit()
        sys.exit()
root = Tk()
root.title("飞机大战")
cv=Canvas(root,width=512,height=294)
img10=PhotoImage(file="images/1.png")
cv.create_image(260,150,image=img10)
cv.pack()
# 创建PanedWindow对象
logo = PhotoImage(file="images/LOGO.png")
logo1=Label(root,image=logo).pack()
pw = PanedWindow(orient=HORIZONTAL)
# 创建labelFrame当做子对象
# 左边包含的
def game11():
    game11=Toplevel()
    game11.title("关卡选择")
    background1  =PhotoImage(file="images/diyiguan.png")
    background2 =PhotoImage(file="images/dierguan.png")
    guankalabel=Label(game11,text="难度选择",font=300,pady=30).pack()
    diyiguanbutton=Button(game11,image=background2,command=start).pack()
    dierguanbutton=Button(game11,image=background1,command=start2).pack()
    game11.mainloop()
def gameinfo():
    gameinfo=Toplevel()
    gameinfo.title("游戏说明")
    background1 = PhotoImage(file="images/Icon-114.png")
    ranklabelimage=Label(gameinfo,image=background1).pack()
    infolabel=Label(gameinfo,text="1.按键操作：wasd移动上下左右也可以移动\n2.如何开始游戏加载完毕点击开始游戏即可开始游戏。\n3.游戏目标合理操作，消灭所有的敌人吧!",font=150)
    infolabel.pack()
    gameinfo.mainloop()
leftframe = LabelFrame(pw, text="游戏",font=66,padx=20,pady=20)
leftButton1 = Button(leftframe, text="开始游戏\n\n飞机大战",font=66,width=12, pady=20,command=game11 ).pack()
leftButton2 = Button(leftframe, text="游戏说明",font=66,width=12, pady=10,command=gameinfo).pack()
# leftButton3 = Button(leftframe, text="按钮3",font=66,width=12, pady=10).pack()
leftframe.pack()
pw.add(leftframe)
# 中间布局和功能
# 分数数据读取，写入
######################################################################################
def rankmode():#rank.txt文件读取，使用with，with执行完灰关闭文件，减少占用
    global list1
    with open(file='rank/rank.txt',mode='r')as f:
        list1=f.read()
rankmode()
def rank():#rank.txt数据返回到list1
    rankmode()
    return (list1)
def rankmodeui():#分数的界面
    rank=Toplevel()
    rank.title("历史分数")
    background1 = PhotoImage(file="images/ui_new_word_png (2).png")
    val=StringVar()
    val.set(list1)
    ranklabelimage=Label(rank,image=background1).pack()
    ranklabel=Label(rank,textvariable=val,font=150).pack()
    rank.mainloop()
######################################################################################
midframe = LabelFrame(pw, text="分数",font=66,padx=20,pady=20)
midButton1 = Button(midframe, text="历史分数",font=66, width=12, pady=10,command=rankmodeui).pack()
midButton2 = Button(midframe, text="按钮1", font=66,width=12, pady=10,state=DISABLED).pack()
midButton3 = Button(midframe, text="按钮1",font=66, width=12, pady=10,state=DISABLED).pack()
midframe.pack()
pw.add(midframe)
# 右边包含
#声音的处理
######################################################################################
def settingmusicon():#设置中的声音开启
    loadmusic()
    waveat()
def settingmusicoff():#设置中的声音关闭
    if judgemusicin == 1:
        wavpause()
        time.sleep(1)
        pygame.mixer.quit()
    else:
        pygame.mixer.quit()
def loadmusic():#挂载混音器
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
def unloadmusic():#卸载混音器
    pygame.mixer.quit()
def waveat():#声音
    waveat = pygame.mixer.Sound("audio/eat.wav")
    waveat.play()
def wavpause():#声音
    wavpasue = pygame.mixer.Sound("audio/zanting.wav")
    wavpasue.play()
def judgemusic():#混音器的开启关闭判断及返回的文本
    global judgemusicin,info# 全局变量判断音频是否关闭
    judgemusicin = 1
    if pygame.mixer.get_init() == None:
        judgemusicin = 0
        info="当前音效状态为：关闭"
    else:
        judgemusicin = 1
        info="当前音效状态为：开启"
loadmusic()
def DEBUG():# 程序调试 ，类似print，因为写了面以后看不到print的反馈
    DEBUG=Toplevel()
    DEBUG.title("调试")
    DEBUG.geometry("300x210")
    DEBUGPRINT = Label(DEBUG, text=info)
    DEBUGPRINT.pack()
    DEBUG.mainloop()
######################################################################################
def music():#音效设置的界面
    music=Toplevel()
    music.title("音效设置")
    judgemusic()
    musiclabel = Label(music,text=info)
    musicbuttonon=Button(music,text="开启音效",command=settingmusicon)
    musicinfo = Button(music,text="关闭音效",command=settingmusicoff)
    if judgemusicin == 0:
        musicinfo.config(state=DISABLED)
    else:
        musicinfo.config(state=NORMAL)
    musicbuttonon.pack()
    musicinfo.pack()
    musiclabel.pack()
    music.mainloop()
rightframe = LabelFrame(pw, text="设置",font=66,padx=20,pady=20)
rightButton1 = Button(rightframe, text="音效",font=66, width=12, pady=10,command=music).pack()
rightButton2 = Button(rightframe, text="背景音乐选择",font=66,width=12, pady=10,state=DISABLED).pack()
rightButton3 = Button(rightframe, text="调试",font=66, width=12, pady=10,command=DEBUG).pack()
rightframe.pack()
pw.add(rightframe)
pw.pack()
root.mainloop()