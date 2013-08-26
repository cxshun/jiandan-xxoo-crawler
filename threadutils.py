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
    
    def startthreadforwriting(self,filename,queuelist,confdict):
        '''
        使用进行把队列写入文件
        '''
        while True:
            time.sleep(int(confdict["autosave"]))
            wu = writingutils()
            #把队列（包括等待和完成）写入到文件中，用于恢复使用
            wu.writetofile(confdict["confdir"] + "/" + filename,queuelist)
            print ("保存列表到文件结束")
            
    def startcrawlurl(self,confdict):
        while True:
            '''
            通过xpath取得需要处理的URL
            '''
            self.processlistdict["waitingurllist"].append(confdict["starturl"])
            for url in self.processlistdict["waitingurllist"]:
                if not url in self.processlistdict["finishedurllist"]:
                    print ("读取网页:" + url)
                    #url的读取，进行xpath的选择，取得页面的翻页选项
                    content = urllib.request.urlopen(url).read().decode(confdict["encoding"])
                    doc = lxml.html.fromstring(content)
                    urllist = doc.xpath(confdict["urlxpath"])
                    
                    #从等待列表移除，并添加到完成列表中
                    self.processlistdict["waitingurllist"].extend(urllist)
                    self.processlistdict["finishedurllist"].append(url)
                    
                    print ("读取网页:" + url + "的图片列表")
                    #图片的读取
                    imgsrclist = doc.xpath(confdict["imgxpath"])
                    self.processlistdict["waitingimglist"].extend(imgsrclist)

    def startwritingthread(self,confdict):
        '''
        启动线程进行相关信息的保存 
        '''
        #启动线程，把队列(包括等待和完成队列)写入到文件    
        t1 = threading.Thread(target = self.startthreadforwriting,args = ("waitingurl.txt",
                                                                             self.processlistdict["waitingurllist"],confdict))  
        t2 = threading.Thread(target = self.startthreadforwriting,args = ("waitingimg.txt",
                                                                             self.processlistdict["waitingimglist"],confdict))
        t3 = threading.Thread(target = self.startthreadforwriting,args = ("finishedurl.txt",
                                                                             self.processlistdict["finishedurllist"],confdict)) 
        t4 = threading.Thread(target = self.startthreadforwriting,args = ("finishedimg.txt",
                                                                             self.processlistdict["finishedimglist"],confdict))      
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()  

    def startcrawlimg(self,confdict):
        '''
        进行图片的保存
        '''
        while True:
            for imgurl in self.processlistdict["waitingimglist"]:
                if not imgurl in self.processlistdict["finishedimglist"]:
                    wu = writingutils()
                    wu.saveimgtofile(imgurl, self.processlistdict, confdict)
                        
