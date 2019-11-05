import MapReduce
import sys
import re
import string


mr = MapReduce.MapReduce()
count=1

def mapper(each_tweet):
    global count
    counter = {}
    for key in each_tweet:
        if key=="text":
            d=[]
            for word in each_tweet[key].split(" "):
                p=[]
                url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))')
                retw=re.compile("(?<!RT\s)@\S+")
                if url.match(word) or word.startswith('#') or retw.match(word) or word=="RT" or word.startswith('@') or word.startswith("retweet"):
                    continue
                word=word.lower()
                word=word.encode('UTF-8').translate(None,string.punctuation)
                if word=="":
                    continue
                if word in counter:
                    counter[word] += 1
                else:
                    counter[word] = 1

    for word in counter:
        mr.emit_intermediate(word, (count, counter[word]))

    count=count+1


def reducer(key, list_of_values):
    total = 0
    li = []
    for id, value in list_of_values:
        total += 1
        li.append((id, value))
    mr.emit((key, total, li))


if __name__ == '__main__':
    #inputdata = open("shortTwitter.txt")
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)

