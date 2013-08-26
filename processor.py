#coding=utf-8
import threading
import os
from threadutils import threadutils

class urlprocess:
    
    #配置的dict
    confdict = {}
    #线程对象，用于写入等待和完成队列
    tu = threadutils()
    
    def __init__(self):
        '''
        初始化操作，包括读文件等
        '''
        f = open("conf.txt")
        for line in f.readlines():
            #如果不是以#开关的一行，则需要进行读取，否则只当做是注释，不进行处理
            if not line.startswith("#"):
                index = line.find("=")
                key = line[0:index]
                #替换文件末尾的\n
                value = line[index + 1:].strip("\n")
                self.confdict[key] = value        
    
    def checkdir(self):
        '''
        判断配置文件放置的目录是否存在，不存在则进行创建
        '''
        #判断存在配置文件的目录是否存在，不存在的情况下，新建该目录
        if (not os.path.exists(self.confdict["confdir"])):
            os.makedirs(self.confdict["confdir"])
    
if __name__ == "__main__":
    print ("开始运行——读取配置文件")
    pro = urlprocess()
    print ("读取配置文件完成")
    
    pro.checkdir()
    
    tu = threadutils()
    #执行定时任务，把列表写入文件
    tu.startwritingthread(pro.confdict)
    
    #开始进行URL的访问并分析
    crawlurlthread = threading.Thread(target = tu.startcrawlurl, args = (pro.confdict,))
    crawlurlthread.start()
    #开始进行爬图
    crawlimgthread = threading.Thread(target = tu.startcrawlimg, args = (pro.confdict,))
    crawlimgthread.start()
    
    