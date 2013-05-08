import json
import re
import sys

class sentiment_term_deriver:

    def __init__(self):
        self.sent_file = sys.argv[1]#'AFINN-111.txt'
        self.tweet_file = sys.argv[2]#'output.txt' 
        self.score_dict=self.get_scores_dict()
        self.tweets_list=self.get_all_tweets()
    
    
    def get_scores_dict(self):
        scores = {} # initialize an empty dictionary
        for line in open(self.sent_file):
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            scores[term] = float(score)  # Convert the score_dict to an integer.
        self.scores=scores
        return scores


    def get_all_tweets(self):
        twitts = []
        f = open(self.tweet_file)
        h=f.readlines()
        for line in h:
            twittdict=json.loads(line)
            try:
                twitttext = twittdict['text'].encode('utf-8')
                p = re.compile(r'[\n\s\."\?!]*')
                spl = p.split(twitttext)
                while '' in spl:
                    spl.remove('')
                twitts.append(spl)                 
            except KeyError:
                pass
        return twitts


    def count_score(self, textdict):
        count=None
        for word in textdict:
            if word in self.score_dict.iterkeys():
                if count is None:
                    count=0.0
                count+=self.score_dict[word]
        return count
    
    
    def count_score_for_list(self, tweet_list):
        tweet_list_score=[]
        for twitt in tweet_list:
            tweet_list_score.append(self.count_score(twitt))
        return tweet_list_score
          
            
    def extract_new_terms(self, tweet):
        score = self.count_score(tweet)
        if score!=None:
            for word in tweet:
                if word in self.score_dict.iterkeys():
                    pass
                else:
                    self.score_dict[word]=score
                    print word + ' '+'%0.2f' %score


    def contains_unknown(self, tweet_list):
        for tweet in tweet_list:
            for word in tweet:
                if word not in self.score_dict.iterkeys():
                    return True
        return False 


    def extract_all_new_terms(self, tweet_list):
        while self.contains_unknown(tweet_list):
            for tweet in tweet_list:
                self.extract_new_terms(tweet)
            self.extract_all_new_terms(tweet_list)
            
    def occurency_all_terms(self, tweet_list):
        count=0
        for tweet in tweet_list:
            for word in tweet:
                count+=1
        return count
    
    def occurency_term(self, tweet_list, term):
        count=0
        for tweet in tweet_list:
            for word in tweet:
                if word==term:
                    count+=1
        return count
            
        
        
                
deriver=sentiment_term_deriver()
deriver.occurency_all_terms(deriver.tweets_list)
    