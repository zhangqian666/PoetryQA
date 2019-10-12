#-*- coding:utf-8 -*-
import os
import jieba.posseg as pseg
import itertools
import time
from py2neo import Graph,Node,Relationship
from readDict import readallverse
verseset=readallverse()
def frommixwordfindverse(mixlist,verseset):
    start = time.clock()
    print("begin")
    index = 0
    versestringlist = []
    takennum = 0
    if len(mixlist) == 12:
        takennum = 7
    else:
        takennum = 5

    for i in itertools.permutations(mixlist, takennum):
        index = index + 1
        versestring = ""
        for item in i:
            versestring = versestring + item
        if versestring in verseset:
            print(versestring)
            break;
    end = time.clock()
    print(end - start)
    return versestring

if __name__=="__main__":
    start=time.clock()
    print("begin")
    mixlist=["孤","远","寒","山","石","片","城","上","仞","斜","万","一"]
    #mixlist=["千","众","飞","常","花","百","里","入","寻","姓","度","他"]
    #mixlist=["花","多","又","知","多","时","雨","少","落"]
    #mixlist=["竟","思","最","相","长","安","物","夕","此"]
    index=0
    versestringlist=[]
    takennum=0
    if len(mixlist)==12:
        takennum=7
    else:
        takennum=5

    for i in itertools.permutations(mixlist, takennum):
        index=index+1
        versestring=""
        for item in i:
            versestring=versestring+item
        if versestring in verseset:
            print(versestring)
            break;
    end=time.clock()
    print(end-start)
    print(index)
    print(len(mixlist))