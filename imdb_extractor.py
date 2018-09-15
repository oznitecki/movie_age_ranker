from imdb import IMDb
import unicodecsv as csv

NUMBER_OF_MOVIES = input("Enter number of movies: ")
TRAIN_TEST_RATIO = input("Enter number of test batches per each train batch: ")
TRAIN_FILE = raw_input("Enter output train file: ")
TEST_FILE = raw_input("Enter output test file: ")
GOLD_FILE = raw_input("Enter output gold file: ")

def movie_id():
    r = open("data.tsv", "rb")
    tsvreader = csv.reader(r,delimiter="\t")
    numbers = []
    for row in tsvreader:
        if row[1] == 'movie' and not (row[5] == '\\N') and int(row[5]) > 1990:
            numbers.append(row[0].split('t')[2])
        if len(numbers) >= NUMBER_OF_MOVIES:
            break
    r.close()
    return numbers

def make_train_file(db, ids, country,allowedvalues):
    f = open("input/"+TRAIN_FILE+".csv", "wb")
    fieldnames = ['id','title', 'plot', 'mpaa']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i in xrange(NUMBER_OF_MOVIES/TRAIN_TEST_RATIO):
        print("putting movie "+str(i)+" to train")
        movie = db.get_movie(ids[i])
        if movie.has_key('certifications') and movie.has_key('plot'):
            for certification in reversed(movie['certifications']):
                if certification.split(':')[0] == country and certification.split(':')[1] in allowedvalues:
                    mpaa = certification.split(':')[1]
                    plot = ''
                    for summary in movie['plot']:
                        plot += summary.split(':')[0]
                    title = movie['title']
                    writer.writerow({'id':ids[i],'title': title, 'plot': plot, 'mpaa': mpaa})
                    break
    f.close()

def make_test_and_gold_files(db, ids, country,allowedvalues):  
    f = open("input/"+GOLD_FILE+".csv", "wb")
    f2 = open("input/"+TEST_FILE+".csv", "wb")
    fieldnames = ['id','title', 'plot', 'mpaa']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer2 = csv.DictWriter(f2, fieldnames=fieldnames)
    writer.writeheader()
    writer2.writeheader()
    for i in xrange(NUMBER_OF_MOVIES/TRAIN_TEST_RATIO,NUMBER_OF_MOVIES):
        print("putting movie "+str(i)+" to test and gold")
        movie = db.get_movie(ids[i])
        if movie.has_key('certifications') and movie.has_key('plot'):
            for certification in reversed(movie['certifications']):
                if certification.split(':')[0] == country and certification.split(':')[1] in allowedvalues:
                    mpaa = certification.split(':')[1]
                    plot = ''
                    for summary in movie['plot']:
                        plot += summary.split(':')[0]
                    title = movie['title']
                    writer.writerow({'id':ids[i],'title': title, 'plot': plot, 'mpaa': mpaa})
                    writer2.writerow({'id':ids[i],'title': title, 'plot': plot})
                    break
    f.close()

db = IMDb()

numbers = movie_id()
print("number of movies:{}".format(len(numbers)))

allowedvalues = ['G','PG','PG-13','NC-17','R']
make_train_file(db, numbers,'United States',allowedvalues)
print('finished train file')
make_test_and_gold_files(db, numbers,'United States',allowedvalues)
print('finished test and gold files')