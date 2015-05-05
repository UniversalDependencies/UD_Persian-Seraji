# -*- coding:utf-8 -*-
import sys
import codecs
import re
import os

SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))
out8=codecs.getwriter("utf-8")(sys.stdout)
ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

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


def read_replacements(f_name):
    reps={}
    #Read the replacements
    with codecs.open(f_name,"r","utf-8") as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith(u"#"):
                continue
            orig,new=line.split(u"->")
            orig,new=orig.strip(),new.strip()
            if u"." in orig: #specifies a condition
                orig,c=orig.rsplit(u".",1)
            else:
                c=None
            assert (orig,c) not in reps
            reps[(orig,c)]=new
    return reps


def repl_pos(line,pos_reps):
    if (line[POS],line[DEPREL]) in pos_reps:
        line[CPOS]=pos_reps[(line[POS],line[DEPREL])]
    elif (line[POS],None) in pos_reps:
        line[CPOS]=pos_reps[(line[POS],None)]
    else:
        print >> sys.stderr, "Warning: no POS rule for", line[POS], line[DEPREL]

def repl_deprel(line,deprel_reps):
    if (line[DEPREL],line[CPOS]) in deprel_reps:
        line[DEPREL]=deprel_reps[(line[DEPREL],line[CPOS])]
    elif (line[DEPREL],None) in deprel_reps:
        line[DEPREL]=deprel_reps[(line[DEPREL],None)]
    else:
        print >> sys.stderr, "Warning: no deprel rule for", line[DEPREL], line[CPOS]


if __name__=="__main__":

    pos_reps=read_replacements(os.path.join(SCRIPTDIR,"pos_rew.txt"))
    deprel_reps=read_replacements(os.path.join(SCRIPTDIR,"deprel_rew.txt"))

    for sent,comments in read_conll(sys.stdin,0):
        for line in sent:
            repl_pos(line,pos_reps)
            repl_deprel(line,deprel_reps)
        if comments:
            print >> out8, u"\n".join(comments)
        print >> out8, u"\n".join(u"\t".join(l) for l in sent)
        print >> out8

