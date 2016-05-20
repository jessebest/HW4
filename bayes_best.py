# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re, random


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
        self.pos_len=[0,0,0,0]
        self.neg_len=[0,0,0,0]

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
        if os.path.isfile("pos_len"):
            self.pos_len = self.load("pos_len")
        if os.path.isfile("neg_len"):
            self.neg_len = self.load("neg_len")

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
                if len(token_list) < 10:
                    neg_len[0] += 1
                elif len(token_list) < 50:
                    neg_len[1] += 1
                elif len(token_list) < 100:
                    neg_len[2] += 1
                else:
                    neg_len[3] += 1
               
                for token in token_list:
                    if token in self.neg_dict.keys():
                        self.neg_dict[token] += 1
                        self.neg_total += 1
                    else:
                        self.neg_dict[token] = 1
                        self.neg_total += 1



            else:
                self.pos_doc += 1
                if len(token_list) < 10:
                    pos_len[0] += 1
                elif len(token_list) < 50:
                    pos_len[1] += 1
                elif len(token_list) < 100:
                    pos_len[2] += 1
                else:
                    pos_len[3] += 1
                for token in token_list:
                    if token in self.pos_dict.keys():
                        self.pos_dict[token] += 1
                        self.pos_total += 1
                    else:
                        self.pos_dict[token] = 1
                        self.pos_total += 1

        common_words=['I', 'am', 'is', 'he', 'she', 'it', 'this', 'that', 'the', 'was', 'were', 'in', 'on', 'at', 'by', 
        'to', 'for', 'about', 'there', 'and', 'or', 'a', 'an', 'of', 'his', 'her', 'their', 'its', 'my', 'me', 'you', 
        'him', 'who', 'where','which', 'whom', 'be', 'himself', 'herself', 'myself', 'yourself', 'themselves']

        for word in common_words:
            if word in pos_dict:
                pos_total -= pos_dict[word]
                del pos_dict[word]
            if word in neg_dict:
                neg_total -= neg_dict[word]
                del neg_dict[word]



        self.save(self.pos_dict, "Positive")
        self.save(self.neg_dict, "Negative")
        self.save(self.pos_doc, "pos_doc")
        self.save(self.neg_doc, "neg_doc")
        self.save(self.pos_total, "pos_total")
        self.save(self.neg_total, "neg_total")
        self.save(self.pos_len, "pos_len")
        self.save(self.neg_len, "neg_len")


    def ten_cv():
        Filelist = []
        pos_filelist=[]
        neg_filelist=[]
        for FileObj in os.walk("movies_reviews/"):
            Filelist = FileObj[2]
            break

        for path in Filelist:
            if path[7]=='1':
                neg_filelist.append(path)
            else:
                pos_filelist.append(path)

        for i in range(0,10):
            random.seed(i)
            random.shuffle(pos_filelist)
            random.shuffle(neg_filelist)
            pos_training = pos_filelist[i * (len(pos_filelist) / 10):(i + 1) * (len(pos_filelist) / 10)]
            pos_testing = pos_filelist[(i + 1) * (len(pos_filelist) / 10):]
            neg_training = neg_filelist[i * (len(neg_filelist) / 10):(i + 1)*(len(neg_filelist) / 10)]
            neg_testing = neg_filelist[(i + 1) * (len(neg_filelist) / 10)]
            cv_train(pos_training,neg_training)
            cv_classify(pos_testing, neg_testingg)

    def cv_train(self, pos_training, neg_traing):
        pass
    def cv_classify(self, pos_testing, neg_testing):
        pass



    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        token_list = self.tokenize(sText)
        
        #print "the size of pos_dict is", sum(self.pos_dict.values())
        #print " the size of neg_dict is", sum(self.neg_dict.values())
        #print " the total of pos is ", self.pos_total
        #print "the total of neg is ", self.neg_total

        if len(token_list)<10:
            pos_prob = math.log((self.pos_len[0]) / float(self.pos_doc))
            neg_prob = math.log((self.neg_len[0]) / float(self.neg_doc))
        elif len(token_list) < 50:
            pos_prob = math.log((self.pos_len[1]) / float(self.pos_doc))
            neg_prob = math.log((self.neg_len[1]) / float(self.neg_doc))
        elif len(token_list) < 100:
            pos_prob = math.log((self.pos_len[2]) / float(self.pos_doc))
            neg_prob = math.log((self.neg_len[2]) / float(self.neg_doc))
        else:
            pos_prob = math.log((self.pos_len[3]) / float(self.pos_doc))
            neg_prob = math.log((self.neg_len[3]) / float(self.neg_doc))


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
            elif c=="!"or c=="?":
                lTokens.append(sToken)
                sToken=""
                sToken+= c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                #if c.strip() != "":
                    #lTokens.append(str(c.strip()))

        if sToken != "":
            lTokens.append(sToken)

        return lTokens
