from split import read_conll
import sys
import codecs

out8=codecs.getwriter("utf-8")(sys.stdout)

ID,FORM,LEMMA,CPOS,POS,FEAT,HEAD,DEPREL,DEPS,MISC=range(10)

sents=list(read_conll(sys.stdin,0))
train,test,devel=codecs.open("fa-ud-train.conllu","w","utf-8"),codecs.open("fa-ud-test.conllu","w","utf-8"),codecs.open("fa-ud-dev.conllu","w","utf-8")

counter=1
for s,comm in sents:
    if counter%10==0:
        f=test
    elif counter%10==1:
        f=devel
    else:
        f=train
    if comm:
        print >> f, u"\n".join(comm)
    print >> f, u"\n".join(u"\t".join(l) for l in s)
    print >> f
train.close()
test.close()
devel.close()

    
