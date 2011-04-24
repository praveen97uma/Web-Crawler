#!usr/bin/python
from tokenizedocuments import TokenizeDocuments
from shelve import DbfilenameShelf as shelve
import mathutils
from numpy import NaN
#TODO move the mathematical functions to another module
class Indexer(object):
    """
    Class to handle the indexing of the documents stored in the
    database. Indexer will use the tokenizedocuments module to retrieve
    indexes or tokens or terms from the documents.
    
    The point to be noted here is that we do not sort the tokens 
    alphabetically but with their integer ids. What we do here is that we
    have our basis vector which is derived from the unique terms in all
    our documents. The dimension of this vector may be very large i.e of 
    the orders of 1,000s or 10,000s. So, we may choose to filter terms with
    lower frequencies to reduce the dimension.
    Also, we precompute all the document vectors and store them in the database.
    This will help in faster similarity computations. 
     
    """
    def __init__(self, database):
        self.db = database
        self.tokenizer = TokenizeDocuments(database)
        self.vec_length = 0
        self.collection_length = self.set_collection_length(database)
        
    def get_document_keywords(self):
        """
        Return the keywords and their integer ids from the documents stored
        in the database.
        """
        t = self.tokenizer
        #get all tokens from database
        all_terms = t.get_all_terms()
        #determine the frequencies of the documents
        term_freq = t.terms_counter(all_terms)
        #filter tokens with frequency of 1
        t.filter_terms(term_freq, [1])
        #get list of unique tokens
        list_of_terms = term_freq.keys()
        # ids is a dictionary of tokens with their integer ids
        ids = t.assign_id_to_terms(list_of_terms)
        #determine the dimension of the vector in the document space which is
        #basicaly the length of the list_of_terms or ids
        self.vec_length = len(ids)
        #ids is a dictionary with keys being the integer ids and the values
        #as tokens or terms. This dictionary is also stored in another database
        #for a possible future use or reference
        return 0
    
    def set_collection_length(self, database):
        """
        Determines the length of document collection for
        self.collection_length attribute of the class.
        """
        db = shelve(database, 'r')
        temp_file = shelve('temp/terms_integerid','r')
        self.vec_length = len(temp_file['id2term'])
        return len(db.keys())
        
    def yield_documents(self):
            """
            Generator to return a document from the database
            """
            db = shelve(self.db, 'w')
            for document in db.itervalues():
                yield document
            #yield db.itervalues().next()
    def yield_keyword(self):
            temp_file = shelve('temp/terms_integerid','w')
            for value in temp_file['id2term'].itervalues():
                yield value
    
    def calculate_document_frequency(self):
        """
        Calculate the document frequencies of the tokens. Document frequency is
        the number of documents in which a keyword appears. This will be used
        to calculate the inverse document frequencies.
        """
        self.get_document_keywords()
        shelve('doc_frequencies','c')
        doc_freq = shelve('doc_frequencies','w')        
        keywords = self.yield_keyword()
        for i in xrange(0,self.vec_length):
            count = 0
            kw = keywords.next()
            doc_generator = self.yield_documents()
            flag = True
            while flag:
                try:
                    if kw in doc_generator.next().all_terms:
                        count+=1
                except StopIteration:
                    flag = False
            doc_freq[kw] = count
            print kw,count
        doc_freq.close()
    
    
    
    
        
    def set_doc_vector(self):
        """
        Iterates through the documents and sets their document vectors 
        """
        doc_generator = self.yield_documents()
        documents = True
        doc_freq = shelve('doc_frequencies','w')
        shelve('documentVectors','c')
        keyword_database = shelve('temp/terms_to_integer','r')
        keywords = keyword_database['term2id']
        dv = shelve('documentVectors','w')
        db = shelve(self.db, 'w')
        for document in db.itervalues():
            """while documents:
                try:
                    document = doc_generator.next()
                    
                except StopIteration:
                    flag = False
             """
            
            key = document.key
            #print key
            doc_terms = document.unique_terms_freq
    
            tf = 0
            doc_vector = zeros(self.vec_length)
            #print self.vec_length
            #print type(doc_vector)
            for kw in keywords:
                #print kw        
                if kw in doc_terms.keys():
                    tf = doc_terms[kw]
                    term_weight = mathutils.calculate_term_weight(tf, doc_freq[kw], self.vec_length)
                    doc_vector[keywords[kw]] = term_weight
                    #print tf,term_weight,vec_index
 
            doc_vector = mathutils.normalise_vector(doc_vector)
            print doc_vector
            dv[key] = doc_vector
            
i = Indexer('database1')        
#i.calculate_document_frequency()
i.set_doc_vector()    
