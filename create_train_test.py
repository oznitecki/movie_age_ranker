import unicodecsv as csv

def writeFile(inputFileName, trainWriter, testWriter):
    f = open(inputFileName, "rb")
    csvreader = csv.reader(f)
    i = 1
    firstLine = True
    for row in csvreader:
        if firstLine:
            firstLine = False
            continue
        if i % 3 == 0:
            trainWriter.writerow({'id':row[0],'title': row[1], 'plot': row[2], 'mpaa': row[3]})
        else:
            testWriter.writerow({'id':row[0],'title': row[1], 'plot': row[2], 'mpaa': row[3]})
        i += 1
    f.close()
    return

train = open("input/trainAll.csv", "wb")
test = open("input/testAll.csv", "wb")
fieldnames = ['id','title', 'plot', 'mpaa']
writer = csv.DictWriter(train, fieldnames=fieldnames)
writer2 = csv.DictWriter(test, fieldnames=fieldnames)
writer.writeheader()
writer2.writeheader()
writeFile("input/trainG.csv",writer,writer2)
writeFile("input/trainPG.csv",writer,writer2)
writeFile("input/trainPG13.csv",writer,writer2)
writeFile("input/trainR.csv",writer,writer2)
writeFile("input/trainNC17.csv",writer,writer2)
train.close()
test.close()