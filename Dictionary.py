import sys
import flashtext
import re,string
input = sys.argv[1]

#create a Dictionary

keywordProcessor = flashtext.KeywordProcessor()
keywordProcessor.add_keyword("của","OF")
keywordProcessor.add_keyword("thuộc","OF")
keywordProcessor.add_keyword("là","BE")
keywordProcessor.add_keyword("và","AND")
keywordProcessor.add_keyword(",","AND")
keywordProcessor.add_keyword("bằng","EQUAL")
keywordProcessor.add_keyword("=","EQUAL")
keywordProcessor.add_keyword("cm","X")
keywordProcessor.add_keyword("độ","X")

ignore = flashtext.KeywordProcessor()
f = open("verb.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"VERB")
    ignore.add_keyword(t,"VERB")
    t = f.readline().strip()
f.close()
f = open("keywords.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"SHAPE")
    t = f.readline().strip()
f.close()

f = open("pre-Q.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"Q-")
    t = f.readline().strip()
f.close()
f = open("pos-Q.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"-Q")
    t = f.readline().strip()
f.close()
f = open("adj.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"ADJ")
    t = f.readline().strip()
f.close()


f = open("keywords2.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"DECOR")
    t = f.readline().strip()
f.close()
#open file and split words
f = open(input,encoding='UTF-8')
t = f.read()
task = t.split("^")
a=0
while a<len(task):
    r = 0
    print(task[a])
    punc = '''!()[]{};:'"\,<>./?@#$%^&*_~'''
    for char in task[a]:
        if char in punc:
            task[a] = task[a].replace(char,"")
    ignore_found = ignore.extract_keywords(task[a].lower(),span_info=True)
    offset = 0
    print(task[a])
    key_found = keywordProcessor.extract_keywords(task[a].lower(), span_info=True)
    splitted = [task[a]]
    l = 0

    for key,begin,end in key_found:
        k = splitted[-1]
        splitted.pop()
        k = [k[:begin-l],k[begin-l:end-l],k[end-l:]]
        splitted = splitted+k
        l = 0
        for str in splitted:
           l+=len(str)
    i=0
    while i<len(splitted):
        splitted[i]= splitted[i].strip()
        if splitted[i]=="" or keywordProcessor.replace_keywords(splitted[i])=="VERB" :
            splitted.remove(splitted[i])
            i-=1
        i+=1
    splitted_keyword=[]
    pattern = re.compile("(\d+)")
    # split number:
    i=0
    while i<len(splitted):
        index = pattern.search(splitted[i])
        if index is not None:
            begin,l = index.regs[0]
            k = splitted.pop(i)
            if k[l:]!="":
                splitted.insert(i, k[l:])
            if k[begin:l]!="":
                splitted.insert(i,k[begin:l])
            if k[:begin]!="":
                splitted.insert(i,k[:begin])

        i+=1
    #delete unecessary \n
    print(splitted)
    for str in splitted:
        k = keywordProcessor.replace_keywords(str)
        if k.isnumeric():
            splitted_keyword.append("NUMBER")
        elif k == str:
            splitted_keyword.append("ID")
        else:
            splitted_keyword.append(k)


    print(splitted_keyword)
    a+=1
f.close()
#-----------PARSE REQUIRED------------#
