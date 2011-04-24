#!usr/bin/python
from math import log
from numpy import zeros
from numpy import dot
from numpy.linalg import norm

def calculate_term_weight(term_freq, doc_freq, total_doc):
        """
        Calculate the term weight of a token acc to a pre-defined
        formula.
        """
        weight = term_freq * log(total_doc/doc_freq)
        return weight
        
def normalise_vector(vector):
        """
        Returns the normalized vector which is the vector divided by
        its magnitude.
        """
        if norm(vector) == 0:
            return vector
        return vector/norm(vector)
        
        
def get_collection_length(database):
   """
   Returns the number of documents in the collection.
   """
   db = shelve(database,'r')
   return len(db.keys())
