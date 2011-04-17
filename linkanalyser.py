from shelve import DbfilenameShelf as shelve
from Models.document import Document
from hashlib import md5
import logging
class LinkAnalyzer(object):
   """creates abstract documents and feeds their attributes
   """
   
   def __init__(self):
      shelve('database1','c')
      
      
      
   def analyze(self, url, links):
      """creates a document and sets its outgoing links
      """
      self.db = shelve('database1','w')
      key = md5(url).hexdigest()
      #if the document is already in the database, just add its outgoing links
      
      if key in self.db.iterkeys():
         doc=self.db[key]
         doc.insertOL(links)
         #print self.db[key].outgoingLinks
      #if there is no document for the url, create a document and add its outgoing links
      if key not in self.db.iterkeys():
         newDoc = Document(url)
         newDoc.insertOL(links)
         self.db[key]=newDoc
         #print self.db[key].outgoingLinks
      #self.extractLinksfromResponse(url,links)       
      self.db.close()
       
   def extractLinksfromResponse(self, url, links):
      """analyses the incoming links from the response
      """
      for link in links:
         key = md5(link).hexdigest()
         if key in self.db.iterkeys():
            doc=self.db[key]
            doc.insertIL(url)
         else:
            newDo=Document(link)
            newDo.insertIL(url)
            #print type(newDo)
            #print type(key)
            self.db[key]=newDo   
         
      
