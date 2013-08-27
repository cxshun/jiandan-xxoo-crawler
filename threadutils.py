#coding=utf-8
import time
import lxml.html
import urllib.request
import threading
from writingutils import writingutils

class threadutils:
    
    #一系列列表的dict,
    '''
        waitingurllist正在等待处理的url列表
        waitingimglist正在等待处理的图片列表
        finishedurllist已经处理完成的url列表
        finishedimglist已经处理完成的图片列表
    '''
    processlistdict = {"waitingurllist":[],"waitingimglist":[],"finishedurllist":[],"finishedimglist":[]}
    
    def __init__(self,confdict):
        '''
        从文件中读取保存的列表
        '''
        self.confdict = confdict
        wu = writingutils()
        self.processlistdict["waitingurllist"].extend(wu.readfromfile("waitingurl.txt",confdict))
        self.processlistdict["waitingimglist"].extend(wu.readfromfile("waitingimg.txt",confdict))
        self.processlistdict["finishedurllist"].extend(wu.readfromfile("finishedurl.txt",confdict))
        self.processlistdict["finishedimglist"].extend(wu.readfromfile("finishedimg.txt",confdict))
        print ("从文件中加载列表结束")
            
    def startthreadforwriting(self,filename,queuelist):
        '''
        使用进行把队列写入文件
        '''
        while True:
            time.sleep(int(self.confdict["autosave"]))
            wu = writingutils()
            #把队列（包括等待和完成）写入到文件中，用于恢复使用
            wu.writetofile(self.confdict["confdir"] + "/" + filename,queuelist)
            
    def startcrawlurl(self):
        #判断首页是否进行处理过，如果处理过，则不需要再进行处理，这里主要是作为一个入口
        if not self.confdict["starturl"] in self.processlistdict["waitingurllist"]:
            self.processlistdict["waitingurllist"].append(self.confdict["starturl"])
        while True:
            '''
            通过xpath取得需要处理的URL
            '''
            for url in self.processlistdict["waitingurllist"]:
                if not url in self.processlistdict["finishedurllist"]:
                    print ("读取网页:" + url)
                    #url的读取，进行xpath的选择，取得页面的翻页选项
                    content = urllib.request.urlopen(url).read().decode(self.confdict["encoding"])
                    doc = lxml.html.fromstring(content)
                    urllist = doc.xpath(self.confdict["urlxpath"])
                    
                    #从等待列表移除，并添加到完成列表中
                    self.processlistdict["waitingurllist"].extend(urllist)
                    self.processlistdict["waitingurllist"].remove(url)
                    self.processlistdict["finishedurllist"].append(url)
                    
                    print ("读取网页:" + url + "的图片列表")
                    #图片的读取
                    imgsrclist = doc.xpath(self.confdict["imgxpath"])
                    self.processlistdict["waitingimglist"].extend(imgsrclist)
                else:
                    self.processlistdict["waitingurllist"].remove(url)

    def startwritingthread(self):
        '''
        启动线程进行相关信息的保存 
        '''
        #启动线程，把队列(包括等待和完成队列)写入到文件    
        t1 = threading.Thread(target = self.startthreadforwriting,args = ("waitingurl.txt",
                                                                             self.processlistdict["waitingurllist"]))  
        t2 = threading.Thread(target = self.startthreadforwriting,args = ("waitingimg.txt",
                                                                             self.processlistdict["waitingimglist"]))
        t3 = threading.Thread(target = self.startthreadforwriting,args = ("finishedurl.txt",
                                                                             self.processlistdict["finishedurllist"])) 
        t4 = threading.Thread(target = self.startthreadforwriting,args = ("finishedimg.txt",
                                                                             self.processlistdict["finishedimglist"]))      
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()  

    def startcrawlimg(self):
        '''
        进行图片的保存
        '''
        while True:
            for imgurl in self.processlistdict["waitingimglist"]:
                if not imgurl in self.processlistdict["finishedimglist"]:
                    wu = writingutils()
                    wu.saveimgtofile(imgurl, self.processlistdict, self.confdict)
                else:
                    self.processlistdict["waitingimglist"].remove(imgurl)
                        
