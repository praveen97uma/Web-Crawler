#!usr/bin/python
from hashlib import md5 
class Document(object):
   """Document abstract class
   """
   def __init__(self,url):
      self.key=md5(url).hexdigest()
      self.url=url
      self.incomingLinks={}
      self.outgoingLinks={}
      self.numberofIL=0
      self.numberofOL=0
      self.docType=''
      
   def insertIL(self,link):
      """method to insert incoming or outgoing links into the document
      """
      if link not in self.incomingLinks.itervalues():
         self.incomingLinks[md5(link).hexdigest()]=link
         self.numberofIL+=1
      
   def insertOL(self,links):
      """method to insert an outgoing link
      """
      #print links
      self.outgoingLinks=dict([(md5(url).hexdigest(),url) for url in links])
      #print self.outgoingLinks
      self.numberofOL+=len(links)
      
      
   
