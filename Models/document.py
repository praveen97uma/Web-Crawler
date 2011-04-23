#!usr/bin/python
from hashlib import md5
from numpy import zeros 
class Document(object):
    """
    Document abstract class.
    all_terms stores all the words in the document.
    unique_terms_freq stores the frequencies of each unique term in the
    document.
    """
    def __init__(self,url):
        self.key = md5(url).hexdigest()
        self.url = url
        self.incomingLinks = {}
        self.outgoingLinks = {}
        self.numberofIL = 0
        self.numberofOL = 0
        self.docType = ''
        self.all_terms = []
        self.unique_terms_freq = {}
      
    def insertIL(self,link):
        """
        Method to insert incoming or outgoing links into the document
        """
        if link not in self.incomingLinks.itervalues():
            self.incomingLinks[md5(link).hexdigest()]=link
            self.numberofIL+=1
      
    def insertOL(self,links):
        """
        Method to insert an outgoing link
        """
        #print links
        self.outgoingLinks=dict([(md5(url).hexdigest(),url) for url in links])
        #print self.outgoingLinks
        self.numberofOL+=len(links)
      
      
   
