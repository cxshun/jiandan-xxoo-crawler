#coding=utf-8
import lxml.html
import threading
from threadutils import threadutils

class urlprocess:
    
    #需要进行处理的队列
    waitingqueue = []
    #已经处理完成的URL
    finishedqueue = []
    #配置的hashtable
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
                key = line.split("=")[0]
                #替换文件末尾的\n
                value = line.split("=")[1].strip("\n")
                self.confdict[key] = value
                
    def processxpath(self,content,xpath):
        '''
        通过xpath取得需要处理的URL
        '''
        doc = lxml.html.fromstring(content)
        urllist = doc.xpath(xpath)
        for url in urllist:
            self.waitingqueue.append(url)
        
        #启动线程，把队列(包括等待和完成队列)写入到文件    
        threading.Thread(self.tu.startthreadforwriting,["waiting.txt",self.waitingqueue,self.confdict])   
        threading.Thread(self.tu.startthreadforwriting,["finished.txt",self.finishedqueue,self.confdict])
            
if __name__ == "__main__":
    pro = urlprocess()
    print(pro.confdict)