import re
import time

import requests
from PyQt5 import QtGui, QtCore, QtWidgets
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree

class searchT(QtCore.QThread):
    resultDict = QtCore.pyqtSignal(list)
    def __init__(self, songName):
        super(searchT, self).__init__()
        self.name = songName
    def run(self):
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        chrome = webdriver.Chrome(chrome_options=option)
        chrome.get("https://music.163.com/#/search/m/?s=" + self.name + "&type=1")
        chrome.switch_to.frame("g_iframe")
        time.sleep(0.5)
        html = chrome.execute_script("""return document.documentElement.outerHTML""")
        chrome.quit()
        html = etree.HTML(html)
        # 歌曲id
        songidList = html.xpath("//div[@class=\"td w0\"]/div/div/a[1]/@href")
        # 歌曲名称
        songNameList = html.xpath("//div[@class=\"td w0\"]/div/div/a[1]/b/@title")
        # 歌手
        singerNameList = html.xpath("//div[@class=\"td w1\"]/div/a[1]/text()")
        # 专辑
        albumList = html.xpath("//div[@class=\"td w2\"]/div/a[1]/@title")
        # 时常
        scList = html.xpath("//div[@class=\"item f-cb h-flag even \"]/div[6]/text()")
        arr = []
        for songid, songName, singerName, album, sc in zip(songidList, songNameList, singerNameList, albumList, scList):
            arr.append({
                "songid": songid[9:],
                "songName": songName,
                "singerName": singerName,
                "album": album,
                "sc": sc
            })
        self.resultDict.emit(arr)

class downMusic(QtCore.QThread):
    _result = QtCore.pyqtSignal(str)
    def __init__(self, id, name, singer):
        super(downMusic, self).__init__()
        self.id = id
        self.name = name
        self.singer = singer
        print(id, name, singer)
    def run(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
        r = requests.get("http://music.163.com/song/media/outer/url?id=" + str(self.id) +".mp3", headers=headers)
        with open("./music/"+self.name+"-"+self.singer+".mp3", "wb") as f:
            f.write(r.content)
            f.close()
        self._result.emit(self.name+"-"+self.singer+"下载完成")