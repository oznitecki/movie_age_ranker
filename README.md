# movie_age_ranker
if you just want to use the program:  
first download output/trigram_diffSets.pkl  
then run user_interface.py and enjoy!

this program user interface takes a movie text description and gives back recommended age rating for the movie by mpaa scale.  
mpaa scale - 'G','PG','PG-13','R','NC-17'  
for scale explanation check https://www.mpaa.org/film-ratings/  
the age ranker learned on imdb database.  
Information courtesy of  
IMDb  
(http://www.imdb.com).  
Used with permission.  

to download data in csv format from imdb:  
first you should update your data.tsv file from https://datasets.imdbws.com/title.basics.tsv.gz  
then run imdb_extractor.py  
Enter the number of movies you want to extract, the test to train ratio, name of output files  
all csv will be created in input directory  
run example:  
Enter number of movies: 3  
Enter number of test batches per each train batch: 2  
Enter output train file: a  
Enter output test file: b  
Enter output gold file: c  
number of movies:3  
putting movie 0 to train  
finished train file  
putting movie 1 to test and gold  
putting movie 2 to test and gold  
finished test and gold files  

to train based on a training csv use one of the trainer files:  
trigram.py, bigram.py, unigram.py, topic-model.py  
the output would be a pickled set of features

to test based on a testing csv use one of the ranker files:  
trigram_ranker.py, bigram_ranker.py, unigram_ranker.py  
the output would be a result csv which can be compared to gold csv

to evaluate results based on a gold csv use evaluate.py  
example output:  
MSE:1.04952322362  
accuracy:0.632728391264  
![AltText](confusion_matrix.png?raw=true)
