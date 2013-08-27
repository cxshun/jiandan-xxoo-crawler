#coding=utf-8
import os
import urllib.request

class writingutils:
    
    def writetofile(self,filename,waitinglist):
        '''
        将队列写入文件中，以方便某些情况下强制退出后的恢复
        '''
        f = open(filename,"w")
        for url in waitinglist:
            f.write(url + "\n")
    
    def readfromfile(self,filename,confdict):
        '''
        从文件中读取保存的队列，用于重新进行处理
        '''
        #判断文件是否存在，如果不存在则不需要进行读取
        if os.path.isfile(confdict["confdir"] + "/" + filename):
            f = open(confdict["confdir"] + "/" + filename,"r")
            savedlist = []
            for line in f.readlines():
                #去掉末尾的\n
                savedlist.append(line.strip("\n"))
            return savedlist
        else:
            return []
    
    def saveimgtofile(self,url,processlistdict,confdict):
        '''
        保存图片在硬盘中，这里的文件夹取得是配置文件中的pic-dir，这里必须要进行配置，否则会报错
        '''
        if url in processlistdict["finishedimglist"]:
            #从等待列表中移除当前的URL
            processlistdict["waitingimglist"].remove(url)
        else:
            picdir = confdict["picdir"]
            filename = url[url.rfind("/") + 1:]
            #把图片写入到文件
            try:
                file = open(picdir + "/" + filename,"w+b")
                file.write(urllib.request.urlopen(url).read())
                #从等待列表中进行移除，并添加到完成列表中
                processlistdict["waitingimglist"].remove(url)
                processlistdict["finishedimglist"].append(url)
            finally:
                file.close()
            