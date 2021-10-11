from tkinter import *               #构建GUI
from tkinter import messagebox as msg  #消息弹窗
import tkinter.font                   #字体设置
import random                        #随机生成
import numpy as np                   #矩阵处理
import os
def drawit():                       #画出一个数独框架
  i=0
  while i<=450:              #每个格子的像素是50*50，9*50=450
      cv.create_line(i,0,i,450)   #画竖向
      cv.create_line(0,i,450,i)    #画横线
      i+=50
      if i%150==0:               #画粗线
          cv.create_line(i,0,i,450,width=3)  #三个格子一个粗线
          cv.create_line(0,i,450,i,width=3)
def create_ans():                #生成完整的数独答案
  mat = np.zeros([9, 9], dtype=np.int)  #创建9*9数组的0数组
  row = [[0] * 9 for i in range(9)]      #定义行，列，格的约束列
  column = [[0] * 9 for i in range(9)]
  gd = [[0] * 9 for i in range(9)]
  DFS(mat, row, column, gd)
  return mat
def dig_holes(num):                #挖洞法
    global mat
    fake_mat=mat.copy()
    seed=[i for i in range (81)]
    row = [[1] * 9 for i in range(9)]
    column = [[1] * 9 for i in range(9)]
    gd = [[1] * 9 for i in range(9)]
    idx=0
    while idx<num:
        if not seed:
            seed = [i for i in range(81)]
            idx=0
            mat=create_ans()
            fake_mat=mat.copy()
        a=random.choice(seed)
        seed.remove(a)
        r=a//9
        c=a%9
        if magic(mat,r,c,fake_mat):
            fake_mat[r][c]=0
            idx+=1
    return fake_mat
def have_try(event):                   #操作尝试系统，定位鼠标位置，确定方格坐标，标红
    global s
    i_x=event.x;
    i_y=event.y;
    grid_i=int(i_x/50)
    grid_j=int(i_y/50)
    if grid_i>8 or grid_j>8: return
    if diged[grid_j][grid_i]==0 :
        cv.create_line(s[1]* 50, s[0]* 50, s[1]* 50 + 50, s[0] * 50,fill='white', width=2)
        cv.create_line(s[1] * 50, s[0] * 50, s[1] * 50, s[0] * 50 + 50, fill='white', width=2)
        cv.create_line(s[1] * 50 + 50, s[0] * 50, s[1]* 50 + 50, s[0] * 50 + 50,fill='white',  width=2)
        cv.create_line(s[1] * 50, s[0] * 50 + 50, s[1] * 50 + 50, s[0] * 50 + 50, fill='white', width=2)
        drawit()
        cv.create_line(grid_i * 50,grid_j*50,grid_i*50+50,grid_j*50,fill='red',width=2)
        cv.create_line(grid_i * 50, grid_j* 50, grid_i * 50 , grid_j *50+ 50,fill='red',width=2)
        cv.create_line(grid_i * 50+50, grid_j * 50, grid_i * 50 + 50, grid_j * 50+50,fill='red',width=2)
        cv.create_line(grid_i * 50, grid_j * 50+50, grid_i * 50 +50, grid_j*50 + 50,fill='red',width=2)
        s=(grid_j,grid_i)
def choose(event):                 #检测系统，防止玩家眼花，没看到数字
    global s
    global modify
    if diged[s[0]][s[1]]==0:
     if event.keycode>48 and event.keycode<59:
       if tip(s[0],s[1],modify,int(event.char)):
           msg.showwarning("温馨小提示","注意！此行或此列或此九宫格数字重复")
       a=Label(cv, text=event.char, font=ft_fill).place(x=10 + s[1] * 50, y=5 + s[0] * 50)
       modify[s[0]][s[1]]=int(event.char)
     elif event.keycode==32 :
       a=Label(cv,text=' ',font=ft_fill).place(x=10 + s[1] * 50, y=5 + s[0] * 50)
       modify[s[0]][s[1]]=0
     for i in range(9):
        for j in range(9):
            if modify[i][j]!=mat[i][j]:
                return
     msg.showinfo("来自艾尔的祝贺","Congraduations!，你真棒")
def DFS(mat,row,column,gd):                  #此处回溯法求解数独
    global li
    for i in range (9):
        for j in range(9):
            if(mat[i][j]==0):
                k=i//3*3+j//3
                random.shuffle(li)
                for n in li:
                    if row[i][n-1]==0 and column[j][n-1]==0 and gd[k][n-1]==0:
                        row[i][n-1]=1
                        column[j][n-1]=1
                        gd[k][n-1]=1
                        mat[i][j]=n
                        if DFS(mat,row,column,gd) :
                            return True
                        row[i][n-1] = 0
                        column[j][n-1] = 0
                        gd[k][n-1] = 0
                        mat[i][j] = 0
                return False
    return True
def magic(mat,r,c,fake_mat):          #优化用户体验，减小判重率
    rn=r//3
    cn=c//3
    save=[]
    for i in range(cn*3,cn*3+3):
        for j in range(9):
            if fake_mat[j][i]==0:
                save.append((j,i))
    for i in range(cn*3,cn*3+3):
        t=r
        num=mat[r][c]
        while True:
            bomb = True
            for j in range(9):
                if (j,i) in save and mat[j][i] == num:
                    t=j
                    if t==r:
                        return False
                    num=mat[t][c]
                    bomb=False
                    break
            if bomb:
                break

    save.clear()
    for i in range(rn*3,rn*3+3):
        for j in range(9):
            if fake_mat[i][j]==0:
                save.append((i,j))
    for i in range(rn * 3, rn * 3 + 3):
        t = c
        num = mat[r][c]
        while True:
            bomb = True
            for j in range(9):
                if (i, j) in save and mat[i][j] == num:
                    t = j
                    if t == c:
                        return False
                    num = mat[r][t]
                    bomb=False
                    break
            if bomb:
                break
    save.clear()
    for i in range(cn*3,cn*3+3):
        if fake_mat[r][i]!=0:
            break
        else:
            save.append(mat[r][i])
    if len(save)==3:
        for i in range(9):
            ans=0
            for j in range(cn*3,cn*3+3):
                if mat[i][j] in save and i!=r:
                    ans+=1
                else:
                    break
            if ans==3:
                return False
    save.clear()
    for i in range(rn*3,rn*3+3):
        if fake_mat[i][c]!=0:
            break
        else:
            save.append(mat[i][c])
    if len(save)==3:
        for i in range(9):
            ans=0
            for j in range(rn*3,rn*3+3):
                if mat[j][i] in save and i!=c:
                    ans+=1
                else:
                    break
            if ans==3:
                return False
    return True
def tip(r,c,try_mat,num):
    rn=r//3
    cn=c//3
    for i in range(9):
        if i!= r and try_mat[i][c]==num:
            return True
    for i in range(9):
        if i!= c and try_mat[r][i]==num:
            return  True
    for i in range(rn*3,rn+3):
        for j in range(cn*3,cn+3):
            if try_mat[i][j]==num:
                return True
    return False
def difficulty():           #难度选择
    global mat
    global diged
    global modify
    drawit()
    for i in range(9):
        for j in range(9):
                a = Label(cv, text=' ', font=ft).place(x=10 + j * 50, y=5 + i * 50)
    c=r.get()
    if c=='1':
        dig=random.randint(30,35)
    if c=='2':
        dig=random.randint(45,46)
    if c=='3':
        dig=random.randint(50,55)
    mat = create_ans()
    diged=dig_holes(dig)
    modify = diged.copy()
    for i in range(9):
     for j in range(9):
        if diged[i][j] != 0:
           a = Label(cv, text=str(diged[i][j]), font=ft).place(x=10 + j * 50, y=5 + i * 50)
def reset():                  #初始化玩家操作
    global  modify
    modify=diged.copy()
    for i in range(9):
        for j in range(9):
            if diged[i][j] == 0:
                a= Label(cv, text=" ", font=ft).place(x=10 + j * 50, y=5 + i * 50)
def key():       #公布答案
    for i in range(9):
        for j in range(9):
            if diged[i][j]==0:
             modify[i][j]=mat[i][j]
             a = Label(cv, text=str(modify[i][j]), font=ft_fill).place(x=10 + j * 50, y=5 + i * 50)
def zibi():   #人性化处理
    op=msg.askyesno("自闭","是否关机")
    if not op:
        msg.showinfo("温馨提示","不行，必须得关机")
    msg.showinfo("温馨提示", "3秒后关机")
    os.system("shutdown -s -t 3")
def fool():
    global color
    global switch
    i = 0
    color = (color + 1) % (len(colors))
    while i <= 450:  # 每个格子的像素是50*50，9*50=450
        cv.create_line(i, 0, i, 450,fill=colors[color])  # 画竖向
        cv.create_line(0, i, 450, i,fill=colors[color])  # 画横线
        i += 50
        if i % 150 == 0:  # 画粗线
            cv.create_line(i, 0, i, 450, width=3,fill=colors[color])  # 三个格子一个粗线
            cv.create_line(0, i, 450, i, width=3,fill=colors[color])
    bu['bg'] = colors[color]
    bu2['bg'] = colors[color]
    bu3['bg'] = colors[color]
    bu4['bg'] = colors[color]
    bu5['bg']=colors[color]
    bu6['bg']=colors[color]
    if switch:
     fuck.after(250, fool)
def happy():
    global switch
    switch=not switch
    if switch:
        fool()
        bu5['text']="停止快乐"
    else:
        bu5['text']="快乐模式"
def tired():
    os.system("choose.dat")
root=Tk()                          #创建一个界面
root.title("数独游戏")               #设置标题
root.geometry('600x550+400+100')    #设置界面大小
colors=('Crimson','LightSkyBlue','SlateBlue','Cyan','Teal','yellow','green','Lime','Olive','Gold','Chocolate','purple')
color=0
cv=Canvas(root,width=450,height=450)  #创建画布
cv.grid(column=0,row=0)             #画布放在左上角
drawit()
li=[i for i in range(1,10)]         #随机选择列表
r=StringVar()                      #选择组件
r.set(1)
ch1=Radiobutton(root,variable=r,value='1',text='简单').place(x=500,y=100)
ch2=Radiobutton(root,variable=r,value='2',text='普通').place(x=500,y=130)
ch3=Radiobutton(root,variable=r,value='3',text='大师').place(x=500,y=160)
bu=Button(root,text="难度选择",command=difficulty)
bu.place(x=500,y=200)
bu2=Button(root,text="一键重置",command=reset)
bu2.place(x=500,y=250)
bu3=Button(root,text="放弃了，公布答案",command=key)
bu3.place(x=70,y=480)
bu4=Button(root,text="自闭了，直接关机吧",command=zibi)
bu4.place(x=240,y=480)
bu5=Button(root,text="快乐模式",command=happy)
bu5.place(x=500,y=300)
bu6=Button(root,text="不好玩，开飞机模式",command=tired)
bu6.place(x=410,y=480)
switch=0
s=(-1,-1)   #初始化选择位置，红色标记
ft=tkinter.font.Font(family='Fixdsys',size=25,weight='bold')   #随机生成的数字字体黑体变大加粗
ft_fill=tkinter.font.Font(family='Fixdsys',size=20)        #玩家自己尝试的数字字体
diged= np.zeros([9, 9], dtype=np.int)
mat= np.zeros([9, 9], dtype=np.int)
modify=diged.copy()
root.bind('<Button-1>',have_try)
root.bind('<KeyPress>',choose)
fuck=Frame(root,height=550,width=600)
root.mainloop()
