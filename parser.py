#!/usr/bin/python
"""
Contains classes for extraction of termd from the documents
"""
import urllib
import formatter
import htmllib
import cStringIO
from porter import PorterStemmer
import string
import re
#TODO implement a good algorithm to extact text from html text 
#but not regular expressions as re does not help in parsing every html page
#possible algorithms are VIPS, Readability, Maximum Subsequence 
#Segmentation etc


class ExtractTermsUsingRegExp(object):
    """ 
    Extracts terms from a document using regular expression.
    """
    def __init__(self):
        """
        Initialise the  class parameters
        """
        self.stop_words = open('stopwords.txt').read().split()    
        self.default_filters = [ 
            self.strip_tags, 
            self.strip_punctuation, 
            self.filter_numbers_and_special_characters,
            self.change_case_to_lower,
            self.filter_stop_words, 
            self.stem_words
        ]
        
               
    def strip_punctuation(self, doc):
        """
        Remove the punctuations from the words
        """
        doc = re.sub("([%s]+)" % string.punctuation, " ", doc)
        return doc 

    def strip_tags(self, doc):
        """
        Remove the HTML tags.
        """
        doc = re.sub(r"<([^>]+)>", "", doc)
        return doc 
    
    def filter_numbers_and_special_characters(self, content): 
        """
        Filters the numbers and special characters from 
        the content and returns a list of terms
        """
      
        content = list(content)
        length_of_content = len(content)
        for index in xrange(0, length_of_content):
            if content[index].isalpha()==False:
                content[index] = " "
      #this is our list of all the words
        content = "".join(content)
        return content.split()
    
    def change_case_to_lower(self, content):
        """
        Returns the list of terms in lower case and removes words 
        whose length is less than 2
        """
      #change the case of the terms to lower
        content = [word.lower() for word in content if len(word)>2]
        return content


    def filter_stop_words(self, terms):
        """ 
        Filters the stop words from the list of possible terms
        """ 
        terms = [word for word in terms if word not in self.stop_words]
        return terms
    
    def stem_words(self, terms):
        """
        Remove the suffixes in terms.
        """
        porter_stemmer = PorterStemmer() #we use the porter stemming algoritm
        terms = [porter_stemmer.stem(word) for word in terms]
        return terms 

    def preprocess_doc(self, content):
        """
        Process the document which is in a string form. All the above
        methods are applied to the string to split them into terms 
        for further processing and keyword generation
        """
        
        temp_content = content
        for method in self.default_filters:
            temp_content = method(temp_content)
        return temp_content



class ExtractTerms(object):
    """
    Class to extract terms from a document
    """
    def __init__(self):
        #TODO may be instead of opening a file and reading the stopwords 
        #make a python list of all the words
        self.stop_words = open('stopwords.txt').read().split()
        self.default_filter_methods = [
            self.get_content, 
            self.filter_numbers_and_special_characters, 
            self.change_case_to_lower,
            self.filter_stop_words, 
            self.stem_words
        ]
        self.regexp_extractor = ExtractTermsUsingRegExp()
        
      
    def get_content(self, document):
        """
        Get the content or the text from the document. 
        Document can be Html document or text file
        """
        outstream = cStringIO.StringIO()
        parser = htmllib.HTMLParser(
            formatter.AbstractFormatter(formatter.DumbWriter(outstream))
        )
        parser.feed(document)
        content = outstream.getvalue()
        outstream.close()
        return content

   #keep only the alphabets and remove numbers and special characters
    
    def filter_numbers_and_special_characters(self, content): 
        """
        Filters the numbers and special characters from 
        the content and returns a list of terms
        """
      
        content = list(content)
        length_of_content = len(content)
        for index in xrange(0, length_of_content):
            if content[index].isalpha()==False:
                content[index] = " "
      #this is our list of all the words
        content = "".join(content)
        return content.split()
      
    def change_case_to_lower(self, content):
        """
        Returns the list of terms in lower case and removes words 
        whose length is less than 2
        """
      #change the case of the terms to lower
        content = [word.lower() for word in content if len(word)>2]
        return content


    def filter_stop_words(self, terms):
        """ 
        Filters the stop words from the list of possible terms
        """ 
        terms = [word for word in terms if word not in self.stop_words]
        return terms
    
    def stem_words(self, terms):
        """
        Remove the suffixes in terms.
        """
        porter_stemmer = PorterStemmer() #we use the porter stemming algoritm
        terms = [porter_stemmer.stem(word) for word in terms]
        return terms 
       
    def count_term_frequencies(self, terms, document):
        """
        Counts the frequencies of each term in terms in the document
        """
        all_terms = self.get_terms(document)
        term_frequencies = {}
        term_frequencies = dict([(term, all_terms.count(term)) for term in terms])
        return term_frequencies  

    def get_terms(self, document):
        """
        Returns a list of all words or terms found in the document
        """
        #terms = self.regexp_extractor.preprocess_doc(document)  
        abstForm_terms = document
        for method in self.default_filter_methods:
            abstForm_terms = method(abstForm_terms)
        return abstForm_terms
        
    def get_unique_terms(self, document):
        """
        Get all the unique terms found in the document.
        document is the html page converted into a string
        """
        #regexp_terms = set(self.regexp_extractor.preprocess_doc(document))
        abstForm_terms = document
        for method in self.default_filter_methods:
            abstForm_terms = method(abstForm_terms)
        #abstForm_terms = set(abstForm_terms)
        #return regexp_terms.union(abstForm_terms)
        return list(set(abstForm_terms))
      
if __name__ == '__main__':

    cont = urllib.urlopen('http://www.iitr.ac.in').read()      
    e = ExtractTerms()
    print len(e.get_unique_terms(cont))
    print len(e.get_terms(cont))
    print e.count_term_frequencies(e.get_unique_terms(cont),cont)
