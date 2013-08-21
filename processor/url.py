#coding=utf-8
import lxml.html

class urlprocess:
    
    #需要进行处理的队列
    waitingqueue = []
    #已经处理完成的URL
    finishedqueue = []
    #配置的hashtable
    confdict = {}
    
    def init(self):
        '''
        初始化操作，包括读文件等
        '''
        f = open("../conf.txt")
        for line in f.readlines():
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
    
if __name__ == "__main__":
    pro = urlprocess()
    pro.init()
    print(pro.confdict)