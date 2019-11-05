import sys
import string
import re
import MapReduce

mr = MapReduce.MapReduce()
scores = {}
count=1


def mapper(each_tweet):
    global count
    for key in each_tweet:
        if key=="text":
            for word in each_tweet[key].split(" "):
                if "#" in word:
                    word=word.split("#")[0]
                url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))')
                retw=re.compile("(?<!RT\s)@\S+")
                
                if url.match(word) or word.startswith('#') or retw.match(word) or word=="RT" or word.startswith('@'):
                    continue
                word=word.lower()
                word=word.encode('UTF-8').translate(None,string.punctuation)
                
                if word in scores:
                    mr.emit_intermediate(count,scores[word])
                else:
                    mr.emit_intermediate(count,0)
    count=count+1


def reducer(key, list_of_values):
    tot=0
    for value in list_of_values:
        tot=tot+value
    mr.emit((key,float(tot)))


if __name__ == '__main__':
    afinnfile = open(sys.argv[1])       # Make dictionary out of AFINN_111.txt file.
    #afinnfile = open("AFINN-111.txt")
    for line in afinnfile:
        term, score = line.split("\t")  # The file is tab-delimited. #\t means the tab character.
        scores[term] = int(score)  # Convert the score to an integer.
    tweet_data = open(sys.argv[2])
    #tweet_data = open("output20.txt")
    mr.execute(tweet_data, mapper, reducer)


