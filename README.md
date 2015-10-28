# UD_Persian

## The Persian Universal Dependency Treebank (v1.1) 

The Persian Universal Dependency Treebank (Persian UD) is the converted version of the Uppsala Persian Dependency Treebank (UPDT) (Seraji, 2015). The treebank has its original annotation scheme based on Stanford Typed Dependencies (de Marneffe et al., 2006; de Marneffe and Manning, 2008). The scheme was extended for Persian to include the language specific syntactic relations that could not be covered by the primary scheme developed for English. The treebank consists of 6000 sentence of written texts with large domain variations, in terms of different genres (containing newspaper articles, fictions, technical descriptions, and documents about culture and art) and tokenization. The variations in the tokenization are due to the orthographic variations of compound words and fixed expressions in the language. The original UPDT was developed by Mojgan Seraji, under the supervision of Joakim Nivre and Carina Jahani at Uppsala University. 

Apart from the universal annotation scheme and the general rules in the UD, the Persian UD and the UPDT differ further in tokenization. All words containing unsegmented clitics (pronominal and copula clitics) annotated with complex labels in the UPDT have been separated from the clitics and received distinct labels in the Persian UD.

The conversion of the UPDT to the Universal Dependencies has been carried out semi-automatically. In this process, we used a conversion script for reversing the head and dependent relations in the prepositional modifier (prep) and object of a preposition (pobj). Furthermore, we have used other scripts tailored for Persian to separate different types of clitics from their host. Subsequently we added different rules for rewriting the coarse-grained part-of-speech tags and the dependency labels. In the current release, all the morphological features have been included. Adding lemmas remain as future work. 


## STATISTICAL OVERVIEW OF THE PERSIAN UD
Tree count:  6000  
Word count:  152918  
Token count: 151671  
Dep. relations: 37 of which 7 language specific  
POS tags: 15  
Category=value feature pairs: 14  

## DATA SPLIT
The data has sequentially been split into 10 parts, of which segments 1-8 are used for training (80%), 
9 for development (10%), and 10 for test (10%) sets.

## REFERENCES
1. De Marneffe, Marie-Catherine, Bill MacCartney, and Christopher D. Manning. 2006. Generating typed dependency parses from phrase structure parses. In Proceedings of the 5th International Conference on Language Resources and Evaluation (LREC). 
2. De Marneffe, Marie-Catherine, and Christopher D. Manning. 2008. Stanford Typed Dependencies Representation. In Proceedings of the COLING’08 Workshop on Cross-Framework and Cross-Domain Parser Evaluation. 
3. Seraji Mojgan. 2015. Morphosyntactic Corpora and Tools for Persian. Doctoral dissertation. Studia Linguistica Upsaliensia 16. 


Documentation status: partial 
Data source: semi-automatic 
Data available since: UD v1.1 
License: CC BY-SA 4.0 
Genre: news articles fictions technical descriptions culture art 
Contributors: Seraji, Mojgan; Ginter, Filip; Nivre, Joakim 
