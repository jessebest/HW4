from bayes import *
#from collections import Counter
bc = Bayes_Classifier()
#print "average length of pos doc is ", bc.pos_total//bc.pos_doc
#print "average length of neg doc is ", bc.neg_total//bc.neg_doc
#p=Counter(bc.pos_dict)
#n=Counter(bc.neg_dict)
#print "most common in pos: "
# for k, v in p.most_common():
#     print '%s: %i'%(str(k),v)
# print "most common in neg: "
# for k,v in n.most_common(50):
#     print '%s: %i'%(str(k),v)
result = bc.classify("I love my AI class!")
print result