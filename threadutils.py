#coding=utf-8
import time
from writingutils import writingutils

class threadutils:
    
    def startthreadforwriting(self,filename,queuelist,confdict):
        '''
        使用进行把队列写入文件
        '''
        while True:
            time.sleep(confdict["autosave"]);
            wu = writingutils()
            #把队列（包括等待和完成）写入到文件中，用于恢复使用
            wu.writetofile(filename,queuelist)