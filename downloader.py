import urllib2
from retriever import Retriever
import os
from time import ctime

class Downloader(object):
    log=open("log.txt",'a')
    def __init__(self):
        self.retriever=Retriever()
        
        self.headers = {
                   
                   'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   
                   'Accept' :'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
                   
                   'Accept-Language' : 'fr-fr,en-us;q=0.7,en;q=0.3',
                   
                   'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
                   
                   }
    
    
    def download(self,url):
                          
        reqObj = urllib2.Request(url, None, self.headers)
        try:
            urlObj = urllib2.urlopen(reqObj)
        
            response = urlObj.readlines()
        except Exception:
            return 
        
        file=open(self.retriever.filename(url),'w')
        
        for line in response:
            file.writelines(line)
        print url+ "**** crawled"
        
        self.log.write("%s *** crawled %s \n***"%(ctime(),url))
        file.close()
            
        return 1         

    def CDownload(self,url):
       try:
           file_name=self.filename(url)
           os.system("curl %s -o %s"%(url,file_name))
           response=open(file_name,"r").read()
       except IOError:
           return 0
       
       return response 

   
   