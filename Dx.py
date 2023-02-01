# Author:PanDaoxi 
from sys import exit
from tkinter import *
from easygui import *
from PIL import Image as img
from base64 import b64decode
from os import name, system, remove
from os.path import exists, splitext
from tkinter.filedialog import askopenfilename

#===============================================================================
# 程序变量设置
system("chcp 65001")
true, false = True, False
title = "Dx 磁盘图标修改工具"
d = lambda t : b64decode(t).decode()

t1 = d(b'5qyi6L+O5L2/55SoIER4IOejgeebmOWbvuagh+S/ruaUueW3peWFt++8gQ==')
t2 = d(b'5oKo5Y+v5Lul5L2/55So5q2k5bel5YW35a+55oKo55qE56OB55uY5Zu+5qCH6L+b6KGM6Ieq5a6a5LmJ55qE5pu05pS544CCCuWmguaenOaCqOaDs+e7p+e7re+8jOivt+eCueWHu+S4i+aWueeahOKAnOeri+WNs+W8gOWni+KAneaMiemSruS7pee7p+e7reOAgg==')
t3 = d(b'6YCJ5oup5L2g5oOz6KaB5L+u5pS55Zu+5qCH55qE55uY56ym77ya')
t4 = d(b'W2F1dG9ydW5dCmljb249ZHJpdmVpY29uLmljbyww')
#===============================================================================

def findDrives():
    dr = []
    for i in range(65, 94):
        t = chr(i) + ":/"
        if exists(t):
            dr.append(t)
    return dr

def makeAutorun():
    drs = findDrives()
    getdr = multchoicebox(t3, title, drs)
    while not getdr:
        if buttonbox("确认退出创建？", title, ["Yes", "No"]) != "No":
            return
        else:
            getdr = multchoicebox(t3, title, drs)
    cho = buttonbox("选择修改方式：", title, ["为每个盘符单独修改图标", "使用同一图标"])
    while not cho:
        if buttonbox("确认退出？", title, ["Yes", "No"]) != "No":
            return
        else:
            cho = buttonbox("选择修改方式：", title, ["为每个盘符单独修改图标", "使用同一图标"])
    if cho == "为每个盘符单独修改图标":
        for i in getdr:
            getf = askopenfilename(title="为 %s 设定图标" % i, filetypes=[["图片类", ".jpg .jpeg .png .bmp .gif"],])
            while not getf:
                if buttonbox("确认退出？", title, ["Yes", "No"]) != "No":
                    return
                else:
                    getf = askopenfilename(title="为 %s 设定图标" % i, filetypes=[["图片类", ".jpg .jpeg .png .bmp .gif .ico"],])
            try:
                img.open(getf).save("%sdriveicon.ico" % i)
                with open("%sautorun.inf" % i, "w", encoding="utf-8") as f:
                    f.write(t4) 
                system("attrib +s +h /s /d %sdriveicon.ico && attrib +s +h /s /d %sautorun.inf" % (i, i))
            except:
                pass
            if exists("%sautorun.inf" % i) and exists("%sdriveicon.ico" % i):
                msgbox("成功！重启电脑后生效。", title)
            else:
                msgbox("失败！可能的原因有：\n(1)磁盘被写保护；\n(2)杀毒软件阻止；\n(3)磁盘空间已满或被设置只读。\n(4)如果 C 盘出现异常，请您使用管理员权限打开此程序。\n\n请修改后再次尝试。", title)
    else:
        getf = askopenfilename(title="为 所有磁盘 设定图标", filetypes=[["图片类", ".jpg .jpeg .png .bmp .gif"],])
        err = []
        while not getf:
            if buttonbox("确认退出？", title, ["Yes", "No"]) != "No":
                return
            else:
                getf = askopenfilename(title="为 所有磁盘 设定图标", filetypes=[["图片类", ".jpg .jpeg .png .bmp .gif .ico"],])
        for i in getdr:
            try:
                img.open(getf).save("%sdriveicon.ico" % i)
                with open("%sautorun.inf" % i, "w", encoding="utf-8") as f:
                    f.write(t4) 
                system("attrib +s +h /s /d %sdriveicon.ico && attrib +s +h /s /d %sautorun.inf" % (i, i))
                if not (exists("%sautorun.inf" % i) and exists("%sdriveicon.ico" % i)):
                    err.append(i)
            except:
                pass
        if len(err):
            msgbox("任务完成，但是部分磁盘设定时出现错误：\n%s\n\n可能的原因有：\n(1)磁盘被写保护；\n(2)杀毒软件阻止；\n(3)磁盘空间已满或被设置只读。\n(4)如果 C 盘出现异常，请您使用管理员权限打开此程序。\n\n请修改后再次尝试。" % "  ".join(err), title)
        else:
            msgbox("任务完成，未出现错误。设定将在电脑重启后生效！", title)
            
def removeAutorun():
    err = []
    drs = findDrives()
    getdr = multchoicebox("选择需要恢复原始图标的磁盘：", title, drs)
    while not getdr:
        if buttonbox("确认退出？", title, ["Yes", "No"]) != "No":
            return
        else:
            getdr = multchoicebox(t3, title, drs)
    for i in getdr:
        try:
            system("attrib -s -h /s /d %sdriveicon.ico && attrib -s -h /s /d %sautorun.inf" % (i, i))
            remove("%sdriveicon.ico" % i)
            remove("%sautorun.inf" % i)
            if exists("%sdriveicon.ico" % i) or exists("%sautorun.inf" % i):
                err.append(i)
        except:
            pass
    if len(err):
        msgbox("任务完成，但是部分磁盘设定时出现错误：\n%s\n\n可能的原因有：\n(1)权限问题；\n(2)杀毒软件阻止；\n\n请修改后再次尝试。" % "  ".join(err), title)
    else:
        msgbox("任务完成，未出现错误。设定将在电脑重启后生效！", title)
        
def main():
    window = Tk()
    window.title(title)
    window.geometry("600x150")
    window.resizable(false, false)
    
    #===========================================================================
    # 文字和按钮渲染
    Label(window, text=t1, font=("simsun", 18), justify="center").pack(side=TOP)
    Label(window, text=t2, font=("simsun", 15), justify="left").place(x=0, y=45)
    Button(window, text="立即开始", font=("simsun", 15), command=makeAutorun).place(x=50, y=100)
    Button(window, text="恢复原始", font=("simsun", 15), command=removeAutorun).place(x=450, y=100)
    #===========================================================================
    
    window.mainloop()
    
try:
    if name == "nt" and __name__ == "__main__":
        main()
except Exception as e:
    msgbox("发生严重错误，导致程序无法继续运行。\n请在此项目 Github Issues 提出 Bug，并附上以下信息：\n\n%s" % e, title)
    exit()