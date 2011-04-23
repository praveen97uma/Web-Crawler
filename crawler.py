#!usr/bin/env python

from sys import argv
from collections import deque
from retriever import Retriever
from urlparse import urlparse
from time import ctime
from downloader import Downloader
from os.path import splitext
import logging
import linkanalyser
class Crawler(object):
    """crawler goes out to the web and downloads the web pages
    """
    _invalidExt = [
        '.pdf', 'jpg', 'jpeg', '.doc', 'docx', 
        '.gif', '.zip', '.rar', '.PDF'
    ]
    def __init__(self):
        self.visited_links = []
        self.links_queue = deque([])
        self.domain = ''
        self.same_domain = True
        self.pageRetriever = Retriever()
        self.downloader = Downloader()
        self.linkanalyser = linkanalyser.LinkAnalyzer()
        logging.basicConfig(
            filename = 'crawler.log', 
            format = '%(levelname)s:%(message)s', 
            level = logging.INFO
        )

         
            
    def crawlPage(self, url, same_domain = True):
        
        retrieverResponse = self.downloader.CDownload(url)
        
        if retrieverResponse == 0:
            print retrieverResponse, "Invalid Url.....parsing skipped\n"
            return
        
        self.visited_links.append(url)
        
        try:
            links = self.pageRetriever.getLinks(url)
            self.linkanalyser.analyze(url, links)
        except Exception:
            return
            
        for link in links:
            if link not in self.visited_links:
                if same_domain == True:
                    if urlparse(link)[1] != self.domain:
                        #print link, " *** discarded for crawl .. not in domain"
                        logging.info("%s * discarded for crawl .. not in domain"%link)
                    else:
                        if link not in self.links_queue:
                            if splitext(link)[1] not in self._invalidExt:
                                self.links_queue.append(link)
                                #print link, " *** new link added to crawl queue"
                                logging.info("%s * new link added to crawl queue"%link)
                        else:
                            #print link,"*** discarded already visited"
                            logging.info("%s * discarded already visited"%link)
                    
                if same_domain == False:
                    if link not in self.links_queue:
                        self.links_queue.append(link)
                        #print link," *** new link added to crawl queue"
                        logging.info("%s * new link added to crawl queue"%link)
                    else:
                        #print link,"*** discarded already visited"
                        logging.info("%s *** discarded already visited"%link)
                      
        print "length of queue is ", len(self.links_queue), "len of visited queue is ", \
            len(self.visited_links)
        logging.info("length of queue is %d   length of visited queue is %d"\
            %(len(self.links_queue), len(self.visited_links)))            
                    
                    
    def start_crawl(self, url, same_domain = True):
        self.links_queue.append(url)
        self.domain = urlparse(url)[1] 
        self.same_domain = same_domain              # process links in queue
        while self.links_queue:
            url = self.links_queue.popleft()
            self.crawlPage(url)
            
            
            
def main():
    if len(argv) > 1:
        url = argv[1]
    else:
        try:
            url = raw_input('Enter starting URL: ')
            
        except (KeyboardInterrupt, EOFError):
            url = ''

    if not url: 
        return
    robot = Crawler()
    robot.start_crawl(url)

if __name__ == '__main__':
    main()
