from split import read_conll
import sys
import codecs

out8=codecs.getwriter("utf-8")(sys.stdout)

ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

reference=read_conll(sys.argv[1],0)
split=read_conll(sys.argv[2],0)

def align(sent_ref,sent_splt):
    ref_str=u"   ".join(l[1] for l in sent_ref)
    splt_str=u"   ".join(l[1] for l in sent_splt)
    
    ref_counter=0
    splt_counter=0
    token=[]
    fullstring=None
    while True:
        if sent_ref[ref_counter][FORM]==sent_splt[splt_counter][FORM]:
            if token: #this finishes the token
                token.append(sent_splt[splt_counter])
                print >> out8, u"%s-%s"%(token[0][0],token[-1][0])+u"\t"+fullstring+("\t_"*8)
                print >> out8, u"\n".join(u"\t".join(l) for l in token)
                token=[]
                fullstring=None
            else:
                print >> out8, u"\t".join(sent_splt[splt_counter])
            ref_counter+=1
            splt_counter+=1
        elif sent_ref[ref_counter][FORM].startswith(sent_splt[splt_counter][FORM]):
            if not token: #I have just discovered a new token
                fullstring=sent_ref[ref_counter][FORM]
            token.append(sent_splt[splt_counter])
            sent_ref[ref_counter][FORM]=sent_ref[ref_counter][FORM][len(sent_splt[splt_counter][FORM]):]
            if sent_ref[ref_counter][FORM][0]==u'\u200c':
                sent_ref[ref_counter][FORM]=sent_ref[ref_counter][FORM][1:]
            splt_counter+=1
        else:
            print >> sys.stderr, "fuck", repr(sent_ref[ref_counter][FORM]), repr(sent_splt[splt_counter][FORM])
            print >> sys.stderr, ref_str.encode("utf-8")
            print >> sys.stderr, splt_str.encode("utf-8")            
            assert not token
            print >> out8, u"\t".join(sent_splt[splt_counter])
            splt_counter+=1
        if splt_counter==len(sent_splt):
            break

for (sent_ref,comm_ref),(sent_splt,comm_splt) in zip(reference,split):
    if comm_splt:
        print >> out8, u"\n".join(comm_splt)
    align(sent_ref,sent_splt)
    print >> out8

