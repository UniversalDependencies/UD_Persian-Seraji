# -*- coding:utf-8 -*-
import sys
import codecs
import re
import os

SCRIPTDIR=os.path.dirname(os.path.abspath(__file__))
out8=codecs.getwriter("utf-8")(sys.stdout)

clitics=u"م|ت|ش|اش|مان|تان|شان|م|ام|ی|ای|ه|ست|یم|ایم|ید|اید|ند|اند".split(u"|")
# for i in range(len(clitics)):
#     clitics[i]=clitics[i][::-1]
# pron_re=re.compile(u'^(%s)'%(u"|".join(clitics)),re.U)
clitics=sorted(clitics,key=lambda c: len(c), reverse=True) #sort by length

def cut_clitic(s):
    for c in clitics:
        if s.endswith(c):
            print >> sys.stderr, "match", len(c)
            if len(c)>1:
                print >> sys.stderr, (u"   ".join((s,c,s[len(c):],s[:len(c)]))).encode("utf-8")
            return s[:-len(c)],s[-len(c):]
    else:
        return s,u"???"


def cut_clitic_old(s):
    s_rev=s[::-1]
    match=pron_re.match(s_rev)
    if match==None:
        return s,u"???"
    else:
        assert len(s_rev[match.end():])+len(s_rev[:match.end()])==len(s)
        #print >> sys.stderr, "match",match.start(),match.end(), match.group(1).encode("utf-8"),"    ",s[::-1].encode("utf-8"),"       ",s.encode("utf-8")
        return (s_rev[match.end():])[::-1],(s_rev[:match.end()])[::-1]

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

split_re=re.compile(ur"(/|\\)",re.U)
def parts(deprel):
    deps=split_re.split(deprel)
    if len(deps)==3: #all but one case!
        if deps[1]==u"/":
            return deps[0],deps[2],"RIGHT"
        elif deps[1]==u"\\":
            return deps[0],deps[2],"LEFT"
        else:
            assert False, deps
    else:
        return [deprel] #no-op

ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)
def split_clitics(sent,comments):
    new_sent=[]
    tokens=[] #list of words that initiate a two-word token
    offsets=[0 for _ in sent] #used to renumber tokens
    headmap=[0 for _ in sent] #reassignment of head IDs (offset) used to correct the heads
    for sent_idx,line in enumerate(sent):
        assert len(line)==10
        deps=parts(line[DEPREL])
        if len(deps)==1: #nothing to do
            new_sent.append(line)
            continue
        else:
            #Need to split
            #comments.append(u"###TOKEN###%d-%d\t%s"%(int(line[0]),int(line[0]+1),line[1])+(u"\t_"*7))
            tok,clit=cut_clitic(line[FORM])
            new_sent.append(line[:]) 
            new_sent[-1][FORM]=clit
            new_sent[-1][LEMMA]=u"_"
            new_sent[-1][FEAT]=u"_"
            new_sent[-1][POS]=u"_"
            new_sent[-1][CPOS]=u"CHECK"
            new_sent[-1][DEPREL]=deps[1]
            for idx in range(sent_idx,len(sent)):
                offsets[idx]+=1
            
            #Now add the original token (sans the clitic: todo)
            new_sent.append(line[:])
            new_sent[-1][FORM]=tok
            new_sent[-1][LEMMA]=u"CHECK"
            new_sent[-1][DEPREL]=deps[0]
            #And now decide on the heads
            if deps[2]==u"LEFT": #The left is the head (ie the newly created token)
                headmap[sent_idx]=-1
                new_sent[-1][HEAD]=unicode(sent_idx+1)
                new_sent[-1][DEPREL]=u"SPLTL:"+new_sent[-1][DEPREL]
            elif deps[2]=="RIGHT":
                new_sent[-2][DEPREL]=u"SPLTR:"+new_sent[-2][DEPREL]
                new_sent[-2][HEAD]=unicode(sent_idx+1)

    #Renumber all heads
    for idx,l in enumerate(new_sent):
        if l[HEAD]!=u"0":
            head_0=int(l[HEAD])-1
            head_0+=offsets[head_0]+headmap[head_0]
            l[HEAD]=unicode(head_0+1)
        l[ID]=unicode(idx+1)
    return new_sent
            
if __name__=="__main__":
    for sent,comments in read_conll(sys.stdin,0):
        sent=split_clitics(sent,comments)
        if comments:
            print >> out8, u"\n".join(comments)
        print >> out8, u"\n".join(u"\t".join(l) for l in sent)
        print >> out8


        
        
