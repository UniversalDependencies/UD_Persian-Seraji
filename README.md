# Universal Dependencies for Persian (v2.2)

# Summary
The Persian Universal Dependency Treebank (Persian UD) is based on Uppsala Persian Dependency Treebank (UPDT). The conversion of the UPDT to the Universal Dependencies was performed semi-automatically with extensive manual checks and corrections.

# Introduction
The Persian Universal Dependency Treebank (Persian UD) is the converted version of the <a href="https://sites.google.com/site/mojganserajicom/home/updt "> Uppsala Persian Dependency Treebank (UPDT)</a> (Seraji, 2015). The treebank has its original annotation scheme based on Stanford Typed Dependencies (de Marneffe et al., 2006; de Marneffe and Manning, 2008). The scheme was extended for Persian to include the language specific syntactic relations that could not be covered by the primary scheme developed for English. The treebank consists of ca 6000 annotated and validated sentences of written texts with large domain variations, in terms of different genres (containing newspaper articles, fictions, technical descriptions, and documents about culture and art) and tokenization. The variations in the tokenization are due to the orthographic variations of compound words and fixed expressions in the language.

Apart from the universal annotation scheme and the general rules in the UD, the Persian UD and the UPDT differ further in tokenization. All words containing unsegmented clitics (pronominal and copula clitics) annotated with complex labels in the UPDT have been separated from the clitics and received distinct labels in the Persian UD.

The conversion of the UPDT to the Universal Dependencies has been carried out semi-automatically. In this process, we used a conversion script for reversing the head and dependent relations in the prepositional modifier (prep) and object of a preposition (pobj). Furthermore, we have used other scripts tailored for Persian to separate different types of clitics from their host. Subsequently we added different rules for rewriting the coarse-grained part-of-speech tags and the dependency labels. Morphological features were then mapped semi-automatically. In the current release, lemmas are added for a large number of tokens. This process is further done semi-automatically. The entire process has been manually validated.

# Acknowledgements
The conversion of the UPDT to the Persian UD has been performed by Mojgan Seraji in collaboration with Filip Ginter. The annotations (PoS tags and dependency relations) were manually checked and corrected by Mojgan Seraji. The universal morphological features and lemmas were further added by Mojgan. The process has been carried out in consultation with Joakim Nivre. The original UPDT was also developed by Mojgan Seraji at Uppsala University. Mojgan is deeply thankful to Joakim Nivre and Carina Jahani for their consultations during the development of the UPDT.

#

# STATISTICAL OVERVIEW OF THE PERSIAN UD
Tree count:  5997 <br />
Word count:  152871 <br />
Token count: 151624 <br />
Dep. relations: 37 of which 7 language specific <br />
POS tags: 15 <br />
Category=value feature pairs: 30 <br />


# DATA SPLIT
The data has sequentially been split into 10 parts, of which segments 1-8 are used for training (80%),
9 for development (10%), and 10 for test (10%) sets.

# FEEDBACK AND BUG REPORTS
Please contact mojgan.seraji96@gmail.com for feedback and bug reports.


# REFERENCES
1. De Marneffe, Marie-Catherine, Bill MacCartney, and Christopher D. Manning. 2006. Generating typed dependency parses from phrase structure parses. In Proceedings of the 5th International Conference on Language Resources and Evaluation (LREC).
2. De Marneffe, Marie-Catherine, and Christopher D. Manning. 2008. Stanford Typed Dependencies Representation. In Proceedings of the COLING’08 Workshop on Cross-Framework and Cross-Domain Parser Evaluation.
3. Seraji Mojgan. 2015.  <a href="http://uu.diva-portal.org/smash/get/diva2:800998/FULLTEXT02.pdf"> Morphosyntactic Corpora and Tools for Persian</a>. Doctoral dissertation. Studia Linguistica Upsaliensia 16.
4. Seraji Mojgan, Filip Ginter, and Joakim Nivre. 2016.  <a href="http://www.lrec-conf.org/proceedings/lrec2016/pdf/697_Paper.pdf"> Universal Dependencies for Persian</a>. In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016), pages 2361-2365.





# CHANGELOG
From v1.1 to v1.2, all morphological features have been added. Some errors have further been corrected. <br />
From v1.2 to v1.3, some errors have been corrected. Lemmas have partly been included. <br />
From v1.3 to v1.4, a number of annotation errors are fixed. More lemmas are added. <br />
From v2.1 to v2.2, repository renamed from UD_Persian to UD_Persian-Seraji.



<pre>
=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v1.1
License: CC BY-SA 4.0
Includes text: yes
Genre: news fiction medical legal social spoken nonfiction
Lemmas: manual native
UPOS: converted from manual
XPOS: manual native
Features: manual native
Relations: manual native
Contributors: Seraji, Mojgan; Ginter, Filip; Nivre, Joakim
Contributing: elsewhere
Contact: mojgan.seraji96@gmail.com
===============================================================================
</pre>
