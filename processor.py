#coding=utf-8
import threading
from threadutils import threadutils

class urlprocess:
    
    #一系列列表的dict,
    '''
        waitingurllist正在等待处理的url列表
        waitingimglist正在等待处理的图片列表
        finishedurllist已经处理完成的url列表
        finishedimglist已经处理完成的图片列表
    '''
    processlistdict = {"waitingurllist":[],"waitingimglist":[],"finishedurllist":[],"finishedimglist":[]}
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
    
    def startwritingthread(self):
        '''
        启动线程进行相关信息的保存 
        '''
        #启动线程，把队列(包括等待和完成队列)写入到文件    
        t1 = threading.Thread(target = self.tu.startthreadforwriting,args = ("waitingurl.txt",self.processlistdict["waitingurllist"],self.confdict))  
        t2 = threading.Thread(target = self.tu.startthreadforwriting,args = ("waitingimg.txt",self.processlistdict["waitingimglist"],self.confdict))
        t3 = threading.Thread(target = self.tu.startthreadforwriting,args = ("finishedurl.txt",self.processlistdict["finishedurllist"],self.confdict)) 
        t4 = threading.Thread(target = self.tu.startthreadforwriting,args = ("finishedimg.txt",self.processlistdict["finishedimglist"],self.confdict))      
        
        t1.start()
        t2.start()
        t3.start()
        t4.start()    
            
if __name__ == "__main__":
    print ("开始运行——读取配置文件")
    pro = urlprocess()
    print ("读取配置文件完成")
    tu = threadutils()
    #开始进行URL的访问并分析
    tu.startcrawlurl(pro.confdict["starturl"], pro.processlistdict["waitingurllist"], pro.processlistdict["finishedurllist"],
                     pro.processlistdict["waitingimglist"], pro.processlistdict["finishedimglist"], pro.confdict)
    #执行定时任务，把列表写入文件
    pro.startwritingthread()
    print(pro.confdict)