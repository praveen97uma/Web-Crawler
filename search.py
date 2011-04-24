#!usr/bin/python
"""
This module implements the class for handling the user queries.

temp/terms_to_integer stores the basis vector in a dictionary with the
terms mapped to integers.
"""
from shelve import DbfilenameShelf as shelve
from Models.document import Document
from porter import PorterStemmer
import mathutils
from counter import Counter
from numpy import zeros
from Models.document import Document
from numpy import dot

keyword_database = shelve('temp/terms_to_integer','r')
keywords = keyword_database['term2id'].keys()
vec_length = len(keywords)
porter_stemmer = PorterStemmer()
dv = shelve('documentVectors','r')
doc_database = shelve('database1','r')

def query_parser(query):
    """
    The query string is split into words or terms. The terms are then
    checked if they are present in our basis vector. The terms which are
    found in the basis vector are then mapped to their integer ids and 
    returned as a vector.
    """
   
    query_terms = query.split()
    query_terms = [porter_stemmer.stem(word) for word in query_terms]
    query_terms = [term for term in query_terms if term in keywords]
    query_vec = zeros(vec_length)
    tfs =dict(Counter(query_terms)) 
    for term in query_terms:
        if term in keywords:
            index = keyword_database['term2id'][term]
            weight = tfs[term]
            query_vec[index] = weight
    query_vec = mathutils.normalise_vector(query_vec)
    return (query_vec)

def search_database(query_vec, no_of_res = 10):
    """
    Searches the database and returns atmost 10 relevant documents.
    """
    results = []
    for doc_id in dv.iterkeys():
        value = dot(dv[doc_id], query_vec)
        results.append((doc_id,value)) 
    results = sorted(results, key=lambda k: k[1], reverse = True)
    count = 0
    for n in xrange(no_of_res):
        if results[n][1] != 0:
            count+=1
            print doc_database[results[n][0]].url
    if count == 0:
        print "No results found!!!"
def search():
    find = True

    while find:
        query = raw_input("Search For : ")
        
        search_database(query_parser(query))
        
search()
