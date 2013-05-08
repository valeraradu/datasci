import json
import re
import sys


class sentiment_term_deriver:

    def __init__(self):
        self.sent_file = sys.argv[1]#'AFINN-111.txt'
        self.tweet_file = sys.argv[2]#'output.txt' 
        self.score_dict=self.get_scores_dict()  
    
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
                twitts.append(spl)                 
            except KeyError:
                pass
        return twitts

    def count_score(self, textdict):
        count=0.0
        for word in textdict:
            for key in self.scores:
                if word==key:
                    count+=self.scores[key]
        return count
    
    def count_score_for_list(self, tweet_list):
        for twitt in tweet_list:
            print self.count_score(twitt)
                    
    
                
deriver=sentiment_term_deriver()
deriver.count_score_for_list(deriver.get_all_tweets())