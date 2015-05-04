import sys
import codecs
import re
import os

SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))

out8=codecs.getwriter("utf-8")(sys.stdout)

from split import read_conll

ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)


for sent,comments in read_conll(sys.stdin,0):
    sent=sent[::-1]
    for i,l in enumerate(sent):
        l[ID]=unicode(i+1)
        l[FEAT]=u"_"
        if l[HEAD]!=u"0":
            l[HEAD]=unicode(len(sent)-int(l[HEAD])+1)
    if comments:
        print >> out8, u"\n".join(comments)
    print >> out8, u"\n".join(u"\t".join(l) for l in sent)
    print >> out8

            
