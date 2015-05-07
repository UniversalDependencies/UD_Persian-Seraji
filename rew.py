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
            if u"&" in new:
                new,f=new.split(u"&")
                new,f=new.strip(),f.strip()
            else:
                f=None
            assert (orig,c) not in reps
            reps[(orig,c)]=(new,f)
    return reps


def repl_pos(line,pos_reps):
    global line_counter
    new_pos,new_feat=pos_reps.get((line[POS],line[DEPREL]),(None,None))
    if new_pos is None:
        new_pos,new_feat=pos_reps.get((line[POS],None),(None,None))
    if new_pos is not None:
        line[CPOS]=new_pos
        if new_feat is not None:
            line[FEAT]=new_feat
    else:
        print >> sys.stderr, "Warning line", line_counter, ": no POS rule for", line[POS], line[DEPREL]

def repl_deprel(line,deprel_reps):
    new_deprel,_=deprel_reps.get((line[DEPREL],line[CPOS]),(None,None))
    if new_deprel is None:
        new_deprel,_=deprel_reps.get((line[DEPREL],None),(None,None))
    if new_deprel is not None:
        line[DEPREL]=new_deprel
    else:
        print >> sys.stderr, "Warning: no deprel rule for", line[DEPREL], line[CPOS]


def pobj_ra(sent):
    prep_lvc_ra_heads=set()
    for line in sent:
        if line[DEPREL]==u"prep-lvc-ra":
            prep_lvc_ra_heads.add(line[HEAD])
    for line in sent:
        if line[ID] in prep_lvc_ra_heads and line[DEPREL]==u"pobj-ra":
            line[DEPREL]=u"compound:lvc"
        
if __name__=="__main__":

    pos_reps=read_replacements(os.path.join(SCRIPTDIR,"pos_rew.txt"))
    deprel_reps=read_replacements(os.path.join(SCRIPTDIR,"deprel_rew.txt"))

    line_counter=0
    for sent,comments in read_conll(sys.stdin,0):
        line_counter+=len(comments)
        for line in sent:
            line_counter+=1
            repl_pos(line,pos_reps)
        pobj_ra(sent)
        for line in sent:
            repl_deprel(line,deprel_reps)
        if comments:
            print >> out8, u"\n".join(comments)
        print >> out8, u"\n".join(u"\t".join(l) for l in sent)
        print >> out8
        line_counter+=1

