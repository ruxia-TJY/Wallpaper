"""
    Wallpaper
"""
import requests
import sys
import os.path
import json
import time
import win32api, win32gui, win32con
import random


def configSet():
    '''
        配置 config.json
    :return:
    '''
    config = '{}'
    config = json.loads(config)
    print('开始配置Wallpaper')

    # 更新模式
    print('\n1.bing每日更新：下载bing每日图片作壁纸')
    print('2.随机：在data文件夹内随机选择一张图片作壁纸')
    config["ChangeMode"] = "bing-day"
    ChangeMode = input('请选择一个模式(默认bing每日更新模式)：')
    if ChangeMode == '2':
        config["ChangeMode"] = "random"


    config["AlsoDownloadBing"] = True
    AlsoDownloadBing = input('是否保持下载bing壁纸，无论是否开启随机模式(y/n):')
    if AlsoDownloadBing == 'n' or AlsoDownloadBing == 'N':
        config["AlsoDownloadBing"] = False

    config = json.dumps(config)
    with open('config.json','w') as f:
        f.write(config)
    print('配置已完成！')

def init():
    '''
    初始化检查
    :return:
    '''
    # data文件夹存放下载的图片
    if not os.path.exists('.\\data'):
        os.mkdir('data')

    if not os.path.exists('.\\config.json'):
        print('配置文件 config.json 不存在！')
        configSet()

def downloadbingImg(CheckDayImgIsExist = True):
    '''
    下载bing今日壁纸
    :return:
    '''
    if CheckDayImgIsExist:
        if os.path.exists(os.path.abspath(os.curdir) +  '\\data\\' + time.strftime("%Y-%m-%d") + '.jpg'):
            print('今日壁纸 ' + time.strftime("%Y-%m-%d") + '.jpg 已存在')
            return

    print('正在获取json文件')
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
    jsonr = requests.get(url)
    print('正在解析json文件')
    imgPath = json.loads(jsonr.text)["images"][0]["url"]
    imgurl = "http://cn.bing.com" + imgPath
    print('正在下载图片')
    img = requests.get(imgurl)
    print('正在写入文件')
    with open('data\\' + time.strftime('%Y-%m-%d') + '.jpg','wb' ) as f:
        f.write(img.content)
    print('写入成功！')
    print('下载完成！')

def setWallpaper(imgPath):
    '''
    设置为壁纸
    :param imgPath:要设置为壁纸的路径
    :return:
    '''
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 2：拉伸  0：居中  6：适应  10：填充
    win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # refresh screen
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imgPath, win32con.SPIF_SENDWININICHANGE)
    print('壁纸设置完成')

def getRandomWallpaperPath():
    '''
    随机文件夹随机获取一个文件路径
    :return:
    '''
    rootdir = '.\\data'
    filenameLst = []
    # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            filenameLst.append(os.path.join(parent, filename))
        if len(filenameLst) == 0:
            print('随机库中不存在任何文件')
            return 'no file'

        x = random.randint(0, len(filenameLst) - 1)
    # print('随机文件列表为:' + str(filenameLst))
    path = filenameLst[x]

    if filenameLst[x][1] == '\\':
        path = filenameLst[x][2:]
    ImgPath = os.path.join(os.path.abspath(os.curdir),path)
    return ImgPath


def parse(argv):
    # 打开图片数据文件夹
    for argv_i in argv:
        if argv_i == '-od':
            cmd = 'start explorer ' + os.path.abspath(os.curdir) + '\\data\\'
            os.system(cmd)
            sys.exit(0)
        elif argv_i == '-config':
            configSet()
            sys.exit(0)
        elif argv_i == '-d':
            downloadbingImg()
        elif argv_i == '-random':
            randomPath = getRandomWallpaperPath()
            if randomPath != 'no file':
                imgPath = randomPath
                print('随机路径为:' + imgPath)
                print('正在设置壁纸')
                setWallpaper(imgPath)
            else:
                print('请检查随机文件夹是否存在图片')

def ReadAndDoConfig():
    # 读取配置文件
    with open('config.json', 'r') as f:
        config = f.read()
    config = json.loads(config)

    # 执行配置文件
    if config["ChangeMode"] == "bing-day":
        downloadbingImg()
        imgPath = os.path.abspath(os.curdir) + '\\data\\' + time.strftime("%Y-%m-%d") + '.jpg'
        setWallpaper(imgPath)
    else:
        # 始终下载bing壁纸模式且本地不存在
        if config["AlsoDownloadBing"] == True:
            downloadbingImg()

    if config["ChangeMode"] == "random":
        imgPath = getRandomWallpaperPath()
        if imgPath != 'no file':
            print('随机路径为:' + imgPath)
            setWallpaper(imgPath)

if __name__ == '__main__':
    print('''
Wallpaper
项目地址：https://github.com/ruxia-TJY/Wallpaper
如果您感觉本项目好，欢迎在Github上Star本项目
    ''')
    init()

    if len(sys.argv) == 1:
        ReadAndDoConfig()
    else:
        parse(sys.argv[1:])
