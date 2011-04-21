#!usr/bin/python
"""
This module contains classes for retrieving the links from the 
files downloaded.

filename method returns an absolute path name corresponding to a url.
getLinks returns the links found on the page
"""

from os import makedirs
from os.path import isdir, exists, dirname, splitext
from urlparse import urlparse
import BeautifulSoup


class Retriever(object):
    """
    Downloads the page corresponding to the url passed and saves it in a folder
    """
    
    _invalidExt = [
        '.pdf', 'jpg', 'jpeg', '.doc', 
        'docx', '.gif', '.zip', '.rar', '.PDF'
    ]
   
    def __init__(self):
        self.docs_list = []  
   
    def filename(self, url, default_file = "index.html"):
        """
        Creates a folder corressponding to the url and returns the file name
        """
        purl = urlparse(url)
        file_name = purl[1] + purl[2]    
        folder_name = (purl[1] + purl[2])
 
        if purl[2] == '':
            folder_name += ('/' + default_file)
            file_name += ('/' + default_file)
        elif purl[2] == '/':
            folder_name += default_file
            file_name += default_file
        elif (purl[2])[-1] == '/':
            file_name += ('/' + default_file)

        folder_path = dirname(folder_name)
        
        if not isdir(folder_path):      # create archive dir if nec.
            if not exists(folder_path): 
                makedirs(folder_path)
        return file_name
        
    def getLinks(self, url, tag = "a", attr = "href"):
        """
        Retrieve links from the file on the system corresponding to the url
        """  
        try: 
            response = open(self.filename(url)).read()  #read from the file
        except IOError:
            raise IOError
        parsed_url = urlparse(url)
        domain = parsed_url[0] + '://' + parsed_url[1]
        
        try:
            soup = BeautifulSoup.BeautifulSoup(response)
            l = soup.findAll(tag, href = True)
        except Exception:
            raise Exception
        links = []
       
        for tag in l:
            link = str(tag[attr]) #convert the link to a string
            purl = urlparse(link)
            if purl[1] == '': #if the link is relative make it absolute
                link = domain+link
            #check if the extension is that of a document    
            if splitext(link)[1] in self._invalidExt: 
                self.docs_list.append(link)
                
             #append only the html link
            links.append(link)
                
        
    
        return list(set(links)) #returns only distinct links
         
    def getDocsList(self):
        """
        Return the list of Documents.
        """
        return self.docs_list
    
    
