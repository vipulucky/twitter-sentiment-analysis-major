import re
import sys

maps = dict()
arousal = dict()
dominance = dict()
finn = dict()

def init():   
    with open("words.csv") as f:
        for line in f:
            word = line.split(",");
            maps[word[0]] = word[2];
            arousal[word[0]] = word[4];
            dominance[word[0]] = word[6];
    with open("finn.csv") as f:
        for line in f:
            word = line.split(",");
            finn[word[0]] = word[1];

def analyseANEW(article):
    output = ""
    output += "<b>Tweet: </b>" + article + "<br>"
    values = article
    words = values.split(" ")
    output += "<b>Words: </b>"+str(len(words))+"<br>"
    c=float(0)
    s=float(0)
    for i in range(0,len(words)):
        if words[i] in maps:
            s = s + float(maps[words[i]])
            c += 1
    output += "<h5>ANEW:</h5>Found total of "+str(c)+" words in ANEW lexicon<br>"
    if c == 0:
        avg=0
    else:
        avg = float(s/c)
    output += "<b>Happiness [ANEW] (0 to 10): </b>"+str(avg)+"<br>"
    return [avg,output]
    
def analyseAFINN(article):
    output = ""
    output += "<b>Tweet: </b>" + article + "<br>"
    values = article
    words = values.split(" ")
    output += "<b>Words: </b>"+str(len(words))+"<br>"
    c=float(0)
    s=float(0)
    for i in range(0,len(words)):
        if words[i] in finn:
            s = s + float(finn[words[i]])
            c += 1
    output += "<h5>AFINN:</h5>Found total of "+str(c)+" words in FINN lexicon<br>"
    if c == 0:
        avg=0
    else:
        avg = float(s/c)
    output += "<b>Happiness [AFINN] (-5 to +5): </b>"+str(avg)+"<br>"
    return [avg,output]

result = "<p>"
init()
with open(sys.argv[2]) as f:
	score = 0
	tweets = 0
        for tmp in f:
	    single_score = 0
            tmp = tmp.replace("'"," ")
            tmp = re.sub("(http://|http://www\\.|www\\.)", "", tmp)
            tmp = re.sub("[^A-Za-z0-9 ]", "", tmp)
            if sys.argv[1] == "ANEW":
                data = analyseANEW(tmp)
            elif sys.argv[1] == "AFINN":
                data = analyseAFINN(tmp)
            score = score + data[0]
            if data[0] != 0:
                tweets += 1
            result += data[1] + "<br><hr><br>";
if tweets == 0:
    final_score = 0
else:
    final_score = float(score/tweets)
result = "<header><h5>The Scores: " + str(final_score) + "</h5></header>" + result
print(result+"</p>")
