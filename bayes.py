# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re


class Bayes_Classifier:
    def __init__(self, pos_dict = None, neg_dict = None, pos_total = 0, neg_total = 0, pos_doc = 0, neg_doc = 0):

        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
            cache of a trained classifier has been stored, it loads this cache.  Otherwise,
            the system will proceed through training.  After running this method, the classifier
            is ready to classify input text."""
        if pos_dict:
            self.pos_dict = self.load(pos_dict)
        else:
            self.pos_dict = {}
        if neg_dict:
            self.neg_dict = self.load(neg_dict)
        else:
            self.neg_dict = {}

        self.pos_total = pos_total
        self.neg_total = neg_total
        self.pos_doc = pos_doc
        self.neg_doc = neg_doc
        

    def train(self,trainingset = "movies_reviews/", traininglist = None):
        """Trains the Naive Bayes Sentiment Classifier."""
        if not traininglist:
            Filelist = []
            for FileObj in os.walk(trainingset):
                Filelist = FileObj[2]
                break
        else:
            Filelist = traininglist

        for path in Filelist:
            token_list = self.tokenize(self.loadFile(trainingset + path))
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




        # self.save(self.pos_dict, "Positive")
        # self.save(self.neg_dict, "Negative")
        # self.save(self.pos_doc, "pos_doc")
        # self.save(self.neg_doc, "neg_doc")
        # self.save(self.pos_total, "pos_total")
        # self.save(self.neg_total, "neg_total")

    def ten_cv(self, trainingset = "movies_reviews/"):
        Filelist = []

        for FileObj in os.walk(trainingset):
            Filelist = FileObj[2]
            break
        
        print len(Filelist)

        random.shuffle(Filelist)

        print len(Filelist)

        averageAccuracy = 0
        averagePrecision = 0
        averageRecall = 0
        averageF1 = 0

        for i in range(0,10):
            validationset = Filelist[i * (len(Filelist) / 10) : (i + 1) * (len(Filelist) / 10)]
            traininglist = []
            
            for f in Filelist:
                if f not in validationset:
                    traininglist.append(f)
            
            self.train(traininglist = traininglist)
            true_pos = 0
            true_neg = 0
            false_pos = 0
            false_neg = 0
            for f in validationset:
                text = self.loadFile(trainingset + f)
                guess = self.classify(text)
                if guess == "Positive" and f[7] == "5":
                    true_pos += 1
                elif guess == "Positive" and f[7] == "1":
                    false_pos += 1
                elif guess == "Negative" and f[7] == "1":
                    true_neg += 1
                elif guess == "Negative" and f[7] == "5":
                    false_neg += 1
                else:
                    print "there is something wrong"
                    
            accuracy = (true_pos + true_neg) / float(true_pos + true_neg + false_pos + false_neg)
            precision = true_pos / float(true_pos + false_pos)
            recall = true_pos / float(true_pos + false_neg)
            f1 = (2 * precision * recall) / float(precision + recall)
            
            averageAccuracy += accuracy
            averagePrecision += precision
            averageRecall += recall
            averageF1 += f1
            
        averageAccuracy = averageAccuracy / 10.0
        averagePrecision = averagePrecision / 10.0
        averageRecall = averageRecall / 10.0
        averageF1 = averageF1 / 10.0
        
        print "Average Accuracy: " + averageAccuracy
        print "Average Precision: " + averagePrecision
        print "Average Recall: " + averageRecall
        print "Average F1: " + averageF1
        return (averageAccuracy, averagePrecision, averageRecall, averageF1)


    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        token_list = self.tokenize(sText)
        
        #print "the size of pos_dict is", sum(self.pos_dict.values())
        #print " the size of neg_dict is", sum(self.neg_dict.values())
        #print " the total of pos is ", self.pos_total
        #print "the total of neg is ", self.neg_total


        #total_doc = self.pos_doc + self.neg_doc

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
