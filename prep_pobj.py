# -*- coding:utf-8 -*-
import sys
import codecs
import re
import os

ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))
out8=codecs.getwriter("utf-8")(sys.stdout)

def prep_pobj(tree):
    prep_heads={} #key: prep_token_id  value: its head
    new_prep_heads={}
    for line in tree:
        if line[DEPREL]==u"prep":
            prep_heads[line[ID]]=line[HEAD]
    for line in tree:
        if line[DEPREL]==u"pobj":
            #If this hangs on prep, rehang and rename
            if line[HEAD] in prep_heads:
                assert line[HEAD] not in new_prep_heads
                new_prep_heads[line[HEAD]]=line[ID]
                line[HEAD]=prep_heads[line[HEAD]]
                line[DEPREL]=u"pobj-ra"
    for line in tree:
        if line[ID] in new_prep_heads:
            assert line[DEPREL]==u"prep"
            line[HEAD]=new_prep_heads[line[ID]]
            line[DEPREL]=u"prep-ra"
    return tree

def read_conll(inp,maxsent):
    """ Read conll format file and yield one sentence at a time as a list of lists of columns. If inp is a string it will be interpreted as filename, otherwise as open file for reading in unicode"""
    if isinstance(inp,basestring):
        f=codecs.open(inp,u"rt",u"utf-8")
    else:
        f=codecs.getreader("utf-8")(sys.stdin) # read stdin
    count=0
    sent=[]
    comments=[]
    for line in f:
        line=line.strip()
        if not line:
            if sent:
                count+=1
                yield sent, comments
                if maxsent!=0 and count>=maxsent:
                    break
                sent=[]
                comments=[]
        elif line.startswith(u"#"):
            if sent:
                raise ValueError("Missing newline after sentence")
            comments.append(line)
            continue
        else:
            sent.append(line.split(u"\t"))
    else:
        if sent:
            yield sent, comments

    if isinstance(inp,basestring):
        f.close() #Close it if you opened it

            
if __name__=="__main__":
    for sent,comments in read_conll(sys.stdin,0):
        sent=prep_pobj(sent)
        if comments:
            print >> out8, u"\n".join(comments)
        print >> out8, u"\n".join(u"\t".join(l) for l in sent)
        print >> out8


        
        
