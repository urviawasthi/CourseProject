import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(400)

# LDA Code acquired from https://github.com/priya-dwivedi/Deep-Learning/blob/master/topic_modeling/LDA_Newsgroup.ipynb

stemmer = SnowballStemmer("english")

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

# Tokenize and lemmatize
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result

'''
Putting all the steps for LDA together. 
'''
def run_LDA_on_segment(transcript):
    processed_docs = []
    processed_docs.append(preprocess(transcript))
    dictionary = gensim.corpora.Dictionary(processed_docs)

    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 1, 
                                   id2word = dictionary,                                    
                                   passes = 10,
                                   workers = 2)

    words = ""
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} \nWords: {}".format(idx, topic ))
        print("\n")
        words += topic + " "

    return words
    
    

# if __name__ == '__main__':
#     transcript = "[SOUND] This lecture is a overview of text retrieval methods. In the previous lecture, we introduced the problem of text retrieval. We explained that the main problem is the design of ranking function to rank documents for a query. In this lecture, we will give an overview of different ways of designing this ranking function. So the problem is the following. We have a query that has a sequence of words and the document that's also a sequence of words. And we hope to define a function f that can compute a score based on the query and document. So the main challenge you hear is with design a good ranking function that can rank all the relevant documents on top of all the non-relevant ones. Clearly, this means our function must be able to measure the likelihood that a document d is relevant to a query q. That also means we have to have some way to define relevance. In particular, in order to implement the program to do that, we have to have a computational definition of relevance. And we achieve this goal by designing a retrieval model, which gives us a formalization of relevance. Now, over many decades, researchers have designed many different kinds of retrieval models. And they fall into different categories. First, one family of the models are based on the similarity idea. Basically, we assume that if a document is more similar to the query than another document is, then we will say the first document is more relevant than the second one. So in this case, the ranking function is defined as the similarity between the query and the document. One well known example in this case is vector space model, which we will cover more in detail later in the lecture. A second kind of models are called probabilistic models. In this family of models, we follow a very different strategy, where we assume that queries and documents are all observations from random variables. And we assume there is a binary random variable called R here to indicate whether a document is relevant to a query. We then define the score of document with respect to a query as a probability that this random variable R is equal to 1, given a particular document query. There are different cases of such a general idea. One is classic probabilistic model, another is language model, yet another is divergence from randomness model. In a later lecture, we will talk more about one case, which is language model. A third kind of model are based on probabilistic inference. So here the idea is to associate uncertainty to inference rules, and we can then quantify the probability that we can show that the query follows from the document. Finally, there is also a family of models that are using axiomatic thinking. Here, an idea is to define a set of constraints that we hope a good retrieval function to satisfy. So in this case, the problem is to seek a good ranking function that can satisfy all the desired constraints. Interestingly, although these different models are based on different thinking, in the end, the retrieval function tends to be very similar. And these functions tend to also involve similar variables. So now let's take a look at the common form of a state of the art retrieval model and to examine some of the common ideas used in all these models. First, these models are all based on the assumption of using bag of words to represent text, and we explained this in the natural language processing lecture. Bag of words representation remains the main representation used in all the search engines. So with this assumption, the score of a query, like a presidential campaign news with respect to a document of d here, would be based on scores computed based on each individual word. And that means the score would depend on the score of each word, such as presidential, campaign, and news. Here, we can see there are three different components, each corresponding to how well the document matches each of the query words. Inside of these functions, we see a number of heuristics used. So for example, one factor that affects the function d here is how many times does the word presidential occur in the document? This is called a term frequency, or TF. We might also denote as c of presidential and d. In general, if the word occurs more frequently in the document, then the value of this function would be larger. Another factor is, how long is the document? And this is to use the document length for scoring. In general, if a term occurs in a long document many times, it's not as significant as if it occurred the same number of times in a short document. Because in a long document, any term is expected to occur more frequently. Finally, there is this factor called document frequency. That is, we also want to look at how often presidential occurs in the entire collection, and we call this document frequency, or df of presidential. And in some other models, we might also use a probability to characterize this information. So here, I show the probability of presidential in the collection. So all these are trying to characterize the popularity of the term in the collection. In general, matching a rare term in the collection is contributing more to the overall score than matching up common term. So this captures some of the main ideas used in pretty much older state of the art original models. So now, a natural question is, which model works the best? Now it turns out that many models work equally well. So here are a list of the four major models that are generally regarded as a state of the art original models, pivoted length normalization, BM25, query likelihood, PL2. When optimized, these models tend to perform similarly. And this was discussed in detail in this reference at the end of this lecture. Among all these, BM25 is probably the most popular. It's most likely that this has been used in virtually all the search engines, and you will also often see this method discussed in research papers. And we'll talk more about this method later in some other lectures. So, to summarize, the main points made in this lecture are first the design of a good ranking function pre-requires a computational definition of relevance, and we achieve this goal by designing appropriate retrieval model. Second, many models are equally effective, but we don't have a single winner yet. Researchers are still active and working on this problem, trying to find a truly optimal retrieval model. Finally, the state of the art ranking functions tend to rely on the following ideas. First, bag of words representation. Second, TF and document frequency of words. Such information is used in the weighting function to determine the overall contribution of matching a word and document length. These are often combined in interesting ways, and we'll discuss how exactly they are combined to rank documents in the lectures later. There are two suggested additional readings if you have time. The first is a paper where you can find the detailed discussion and comparison of multiple state of the art models. The second is a book with a chapter that gives a broad review of different retrieval models. [MUSIC]"
#     run_LDA_on_segment(transcript)





