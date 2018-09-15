from imdb import IMDb
import unicodecsv as csv

def movie_id():
    r = open("data.tsv", "rb")
    tsvreader = csv.reader(r,delimiter="\t")
    numbers = []
    for row in tsvreader:
        if row[1] == 'movie' and not (row[5] == '\\N') and int(row[5]) > 1990:
            numbers.append(row[0].split('t')[2])
        if len(numbers) > 20000:
            break
    r.close()
    return numbers

def make_train_file(db, ids, country,allowedvalues):
    f = open("input/train.csv", "wb")
    fieldnames = ['id','title', 'plot', 'mpaa']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for i in xrange(600):
        print(i)
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
    f = open("input/gold4.csv", "wb")
    f2 = open("input/test4.csv", "wb")
    fieldnames = ['id','title', 'plot', 'mpaa']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer2 = csv.DictWriter(f2, fieldnames=fieldnames)
    writer.writeheader()
    writer2.writeheader()
    for i in xrange(5000,20000):
        print(i)
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
print(len(numbers))

allowedvalues = ['G','PG','PG-13','NC-17','R']
#make_train_file(db, numbers,'United States',allowedvalues)
#print('finished train file')
make_test_and_gold_files(db, numbers,'United States',allowedvalues)
print('finished test and gold files')