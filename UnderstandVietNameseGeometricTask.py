import sys
import flashtext
import time
import re
import Dictionary
#----------------THINGS FOR PARSING-------------#
class Trienode():
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.children = dict()
        self.isword=False
    def insert(self,key):
        self.children[key] = Trienode(key,0)
    def query(self):
        r = self.value
        for child in self.children:
            r +=child.query()
        return r
    def search(self,str,index = 0):
        if (index == len(str)):
            self.value+=1
            return True
        c = str[index]
        if c in self.children.keys():
            i =index +1
            return self.children[c].search(str,i)
        else:
            return False
        pass
    def query(self):
        r =0
        if self.value>0 and self.isword:
            r +=1
        for child in self.children.values():
            r+= child.query()
        return r
def intoTrie(str,root):
    pass
    current = root
    com = str.split("->")
    concepts = com[0].strip().split()
    goal = com[1].split()
    for c in range(0, len(concepts)):
        if concepts[c] not in current.children.keys():
            current.insert(concepts[c])
            current = current.children[concepts[c]]
        else:
            current = current.children[concepts[c]]
    current.goals = goal
def chooseStep(stk, cur, root):
    i=0
    j=0
    root_cur = root
    stk_cur = stk[-1]

    while(j<len(stk)) and (stk[j] in root_cur.children.keys()):
        root_cur=root_cur.children[stk[j]]
        j+=1
    # if root_cur.children:
    #     pass
    # else:
    #     if root_cur.goals is not None:
    #         return "Reduce",root_cur.goals,i,j
    #     continue
    # checking grammar in
    if j<len(stk):
        pass
    else:
        if cur in root_cur.children.keys():
           return "shift",None,i,j
        else:
            if root_cur.goals is not None:
                return "Reduce",root_cur.goals,i,j
    return "shift",None,i,j
f = open("DB2.txt",encoding="UTF-8")
task = f.read().split("^")
f.close()
a = 0
root =Trienode('',0)
source = "rule.txt"
f =  open(source, encoding='utf-8')
t = f. readline().strip()
arr = []
while(t!=''):
    intoTrie(t,root)
    t = f.readline().strip()
result = dict()
result_equal =dict()

while a < len(task):
    print(task[a])
    splitted,splitted_keyword = Dictionary.BeforeParser(task[a])
    print(splitted)
    print(splitted_keyword)
    if a==0:
        inp = splitted_keyword
        cur = inp[0]
        stk = []
        if "DIEM" not in result.keys():
            result["DIEM"] = []
        while (1):
            if (stk == []):
                stk.append(inp.pop(0))
                cur = inp[0]
                continue
            name, goal, re_start, re_end = chooseStep(stk, cur, root)
            if goal is not None:
                re_end -= 1
                raw_g = goal
                i = re_start
                while i<=re_end:
                    if stk[i]=="ID":
                        for c in splitted[i]:
                            if c not in result["DIEM"]:
                                result["DIEM"].append(c)
                    i+=1
                for splitted_goal in raw_g:
                    case1Atr = False
                    caseEQUAL = False
                    for c in splitted_goal:
                        if c=="-":
                            case1Atr=True
                        if c=="=":
                            caseEQUAL==True
                    if case1Atr:
                        t = splitted_goal.split("-")
                        r_key = t[0].split("_")
                        r_value = t[1]
                        key = ""
                        for c in r_key:
                            pass
                            key += splitted[int(c)]+ " "
                        key = key.strip()
                        if key not in result.keys():
                            result[key]=[]
                            result[key].append(splitted[int(r_value)])
                        else:
                            result[key].append(splitted[int(r_value)])
                    elif caseEQUAL:
                        splitted_goal.split("=")
                        r_key = splitted_goal[0]
                        r_value = splitted_goal[1]
                        key = r_key.strip()
                        result_equal[key] = r_value
                while (re_start < re_end):
                    stk.pop(re_end)
                    splitted.pop(re_end)
                    re_end -= 1
                stk.pop(re_start)
                splitted.pop(re_start)

            else:
                if cur is None:
                    break
                else:
                    stk.append(inp.pop(0))
                if (inp != []):
                    cur = inp[0]
                else:
                    cur = None
    for key in result.keys():
        print(key,result[key])
    for key in result_equal.keys():
        print("{}={}".format(key,result_equal[key]))
    a+=1

