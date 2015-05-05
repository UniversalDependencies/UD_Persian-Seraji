cat ud-persian-orig.conllu | python lr.py | python split.py | python lr.py | python prep_pobj.py > ud-persian-presplit.conllu
#cat ud-persian-presplit.conllu | python lr.py | python ../Finnish-dep-parser/visualize.py --max_sent 300 > ud-persian-presplit.html

