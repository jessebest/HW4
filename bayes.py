# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re


class Bayes_Classifier:
    def __init__(self):

        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
            cache of a trained classifier has been stored, it loads this cache.  Otherwise,
            the system will proceed through training.  After running this method, the classifier
            is ready to classify input text."""
        self.pos_dict = {}
        self.neg_dict = {}
        self.pos_total = 0
        self.neg_total = 0
        self.pos_doc = 0
        self.neg_doc = 0

        if os.path.isfile("Positive"):
            self.pos_dict = self.load("Positive")
        if os.path.isfile("Negative"):
            self.neg_dict = self.load("Negative")
        if os.path.isfile("pos_doc"):
            self.pos_doc = self.load("pos_doc")
        if os.path.isfile("neg_doc"):
            self.neg_doc = self.load("neg_doc")
        if os.path.isfile("pos_total"):
            self.pos_total = self.load("pos_total")
        if os.path.isfile("neg_total"):
            self.neg_total = self.load("neg_total")

        else:
            self.train()

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        Filelist = []
        for FileObj in os.walk("movies_reviews/"):
            Filelist = FileObj[2]
            break

        for path in Filelist:
            token_list = self.tokenize(self.loadFile("movies_reviews/" + path))
            star = path[7]

            if star == '1':
                self.neg_doc += 1
                for token in token_list:
                    if token in self.neg_dict.keys():
                        self.neg_dict[token] += 1
                        self.neg_total += 1
                    else:
                        self.neg_dict[token]=1
                        self.neg_total+=1



            else:
                self.pos_doc += 1
                for token in token_list:
                    if token in self.pos_dict.keys():
                        self.pos_dict[token] += 1
                        self.pos_total += 1
                    else:
                        self.pos_dict[token]=1
                        self.pos_total+=1




        self.save(self.pos_dict, "Positive")
        self.save(self.neg_dict, "Negative")
        self.save(self.pos_doc, "pos_doc")
        self.save(self.neg_doc, "neg_doc")
        self.save(self.pos_total, "pos_total")
        self.save(self.neg_total, "neg_total")


    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        token_list = self.tokenize(sText)
        
        #print "the size of pos_dict is", sum(self.pos_dict.values())
        #print " the size of neg_dict is", sum(self.neg_dict.values())
        #print " the total of pos is ", self.pos_total
        #print "the total of neg is ", self.neg_total

        


        total_doc = self.pos_doc + self.neg_doc

        pos_prob = 0;
        neg_prob = 0;

        for token in token_list:
            if token in self.pos_dict:
                pos_prob += math.log((self.pos_dict[token] + 1) / float(self.pos_total))
            else:
                pos_prob += math.log(1 / float(self.pos_total))
            if token in self.neg_dict:
                neg_prob += math.log((self.neg_dict[token] + 1) / float(self.neg_total))
            else:
                neg_prob += math.log(1 / float(self.neg_total))
    
        print "pos_prob= ", pos_prob
        print "neg_prob= ", neg_prob

        if pos_prob > neg_prob:
            return "Positive"
        elif pos_prob < neg_prob:
            return "Negative"
        else:
            return "Neutral"


    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt


    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()


    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj


    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))

        if sToken != "":
            lTokens.append(sToken)

        return lTokens
