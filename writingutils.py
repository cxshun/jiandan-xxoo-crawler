#coding=utf-8

class writingutils:
    
    def writetofile(self,filename,queuelist):
        '''
        将队列写入文件中，以方便某些情况下强制退出后的恢复
        '''
        f = open(filename,"w")
        for url in queuelist:
            f.write(url)
    
    def readfromfile(self,filename):
        '''
        从文件中读取保存的队列，用于重新进行处理
        '''
        f = open(filename,"r")
        queuelist = []
        for line in f.readlines():
            #去掉末尾的\n
            queuelist.append(line.strip("\n"))
        return queuelist