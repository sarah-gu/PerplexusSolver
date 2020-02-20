import os
import shutil

source = '/Users/sarahgu/Downloads/traindata'
pictureFinal =  '/Users/sarahgu/Downloads/pictures'
destination = '/Users/sarahgu/Downloads/imagefinal'

for filename in os.listdir(source):
    for file2 in os.listdir(pictureFinal):
        if filename[0:7] == file2[0:7]:
            shutil.move('/Users/sarahgu/Downloads/pictures/' + file2, destination)

