import urllib2
from retriever import Retriever
import os
from time import ctime
import logging
class Downloader(object):
    """There are two downloaders
    download() uses the urllib2 module
    CDownload() uses curl to download the pages. This results in fast page downloads
    """
    def __init__(self):
        self.retriever = Retriever() #to use the filename function
        self.headers = {    
          'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
          'Accept' : 'text/xml,application/xml,application/xhtml+xml,\
            text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
          'Accept-Language' : 'fr-fr,en-us;q=0.7,en;q=0.3',
          'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
        }
    
    
    def download(self,url):
        """downloads the webpage indicated by url and saves it in a 
        file with an absolute path as that of the url
        """                  
        reqObj = urllib2.Request(url, None, self.headers)
        try:
            urlObj = urllib2.urlopen(reqObj)
            response = urlObj.readlines()
        except Exception:
            return 
        #write the content of the response object to the file
        file = open(self.retriever.filename(url), 'w')
        
        for line in response:
            file.writelines(line)
        print url + "**** crawled"
        
        logging.info("* crawled %s \n"%url)
        file.close()
            
        return 1         

    def CDownload(self, url):
        try:
            file_name = self.retriever.filename(url)
            #curl downloads the file and writes it into a file
            os.system("curl %s -o %s"%(url, file_name))
            print url + "**** crawled"
            logging.info("* crawled %s \n"%url)
            response=open(file_name, "r").read()
        except IOError:
            return 0
        
        return response 

   
   
