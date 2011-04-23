#!usr/bin/python 
"""
This module contains the classes for extracting terms from the documents
and store them in their abstract document representation in the database
for future use during indexing
"""
from shelve import DbfilenameShelf as shelve
from retriever import Retriever
import parser
from counter import Counter
class TokenizeDocuments(object):
    """ 
    Store the terms or tokens of a document in its abstract representation.
    This class sets the all_terms and unique_terms attributes of the
    Document model stored in the database while crawling. This will be useful
    when we prepare the set of index terms to decide about the dimension of the
    vectors which will represent the documents. 

    We will take the set intersection of the unique_terms of all the documents. 
    The number of terms or tokens in this resulting set will be our dimension of
    the document vector. The document vector can also include other information
    such as the date, author etc. 
    all_terms will be a dictionary which stores the terms in the unique_terms
    with their frequencies in the document. This will help in determining the 
    term frequency and inverse document frequency for the tf-idf calculations.
    """

    def __init__(self, database):
        self.db = database
        self.retriever = Retriever()
        self.term_extractor = parser.ExtractTerms()

    """This code does not work
    def set_tokens(self):
        
        #Iterate through all the documents and sets its all_terms and unique_terms
        #attributes
        
        self.database = shelve(self.db, 'w')
        for key in self.database.iterkeys():
            abstract_doc = self.database[key]
            url = abstract_doc.url
            document = open(self.retriever.filename(url)).read()
            abstract_doc.all_terms = self.term_extractor.get_terms(document)
            #print abstract_doc.unique_terms
            abstract_doc.unique_terms_freq = self.term_extractor.count_term_frequencies(
                set(abstract_doc.all_terms), document
            )
            print abstract_doc.unique_terms_freq
        self.database.close()
        
        """
          
    def get_all_terms(self, pod = 1):
        """
        Iterate through the documents and retrieve the list of all the terms in
        the corpus of text. pod is the percentage of documents that we want to 
        collect the terms for.  
        """
        self.database = shelve(self.db, 'w')
        no_of_docs_in_database = 0
        for key in self.database.iterkeys():
            no_of_docs_in_database += 1
        no_of_docs = int(pod* no_of_docs_in_database)
      
        def yield_all_terms():
            """
            Generator object which yields the all_terms attributes of the
            documents in the database
            """
            for key in self.database.iterkeys():
                yield self.database[key].all_terms
      
        terms_generator = yield_all_terms()
        all_terms = terms_generator.next()
        #print vector,len(vector)
        for i in xrange(1, no_of_docs):
         #print terms_generator.next(),len(terms_generator.next())
            all_terms.extend(terms_generator.next())
         
        self.database.close()  
        return (all_terms) 
      
    def terms_counter(self, list_of_terms):
        """
        Calculates the frequency of terms in the list of terms
        and returns a counter object.
        """
        freq = Counter(list_of_terms)
        return freq
   
    def filter_terms(self, dict_of_terms, with_frequency = [1]):
        """
        Filters the terms with the frequencies as passed in the parameter
        'with_frequency' from the dict_of_terms which contains that key-value
        pair as the term-frequency and returns a list.

        dict_of_terms is a counter object specifically. 
        """
        remove_terms = [term for term in dict_of_terms.iterkeys() if
            dict_of_terms[term] in with_frequency
        ]
      
        for term in remove_terms:
            dict_of_terms.__delitem__(term)
        return dict_of_terms
        
    def assign_id_to_terms(self, list_of_terms):
        """
        Assign an integer id to all the terms for mathematical manipulation.
        We save the dictionary of integers mapped to the terms in a database 
        for future reference.
        id2term stands for mapping of integer to a term.
        term2id stands for term mapped to an integer.
        """
        terms_to_int = dict(enumerate(list_of_terms))
        shelve('temp/terms_integerid','c')
        temp_file = shelve('temp/terms_integerid','w')
        temp_file['id2term'] = terms_to_int
        temp_file.close()    
        return terms_to_int
         


t = TokenizeDocuments('database1')
#t.set_tokens()
terms = t.get_all_terms()
freq = t.terms_counter(terms)
#print len(list(freq))

(t.filter_terms(freq, [1,2]))

list_of_terms = freq.keys()

ids = t.assign_id_to_terms(list_of_terms)
print ids
#print ids          
