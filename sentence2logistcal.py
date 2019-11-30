# -*- coding:utf-8 -*-
import os
import jieba.posseg as pseg
import jieba
from readDict import readPropertyWord
from readDict import readQuestionWord

from pyltp import Postagger, Parser

from const.controller import LTP_DATA_DIR

jieba.load_userdict('./qadata/userdict.txt')
propertylist, propertydict = readPropertyWord()  # 读取关系词，并做成词典
questionlist, questiondict = readQuestionWord()  # 读取问题词，并做成词典
nertypelist = ['VER', 'POT']


def answerrecognition(sentence, entitylist, poslist, indexset):  # 命名实体识别、抽取句子中的关系词、问题词
    indexlist = []  # 取出indexset中较小的值，组成indexlist
    for index in indexset:
        smallnum = 1000
        for i in index:
            if i < smallnum:
                smallnum = i
        indexlist.append(smallnum)
    allwordlist = entitylist
    allposlist = poslist
    allweilist = indexlist
    resultwordlist = []
    resultposlist = []
    seg_list2 = pseg.cut(sentence)
    jiebawordlist = []
    jiebaposlist = []
    for i in seg_list2:
        jiebawordlist.append(i.word)
        jiebaposlist.append(i.flag)
    index = 0
    while index != len(jiebawordlist):
        word = ""
        if len(allwordlist) != 0:
            word = allwordlist[0]
        if jiebawordlist[index] in word:
            resultwordlist.append(word)
            resultposlist.append(allposlist[0])
            while index < len(jiebawordlist) and jiebawordlist[index] in word:
                index = index + 1
            allwordlist.pop(0)
            allposlist.pop(0)
        elif jiebawordlist[index] in propertylist:
            resultwordlist.append(jiebawordlist[index])
            resultposlist.append("property")
            index = index + 1
        elif jiebawordlist[index] in questionlist:
            resultwordlist.append(jiebawordlist[index])
            resultposlist.append("question")
            index = index + 1
        else:
            resultwordlist.append(jiebawordlist[index])
            resultposlist.append("null")
            index = index + 1

    return resultwordlist, resultposlist


def findproperty(i, arcshead, arcsrela, resultposlist):  # 寻找属性词
    if resultposlist[i] != "property" and arcshead[i] - 1 >= 0:
        i = arcshead[i] - 1
        return findproperty(i, arcshead, arcsrela, resultposlist)
    elif resultposlist[i] != "property" and arcshead[i] - 1 < 0:
        return -1
    else:
        return i


def findobject(i, arcshead, arcsrela, resultposlist):
    if resultposlist[i] not in nertypelist and arcshead[i] - 1 >= 0:
        i = arcshead[i] - 1
        return findproperty(i, arcshead, arcsrela, resultposlist)
    elif resultposlist[i] not in nertypelist and arcshead[i] - 1 < 0:
        return -1
    else:
        return i


def answersemantic(resultwordlist, resultposlist):  # 根据ltp进行句法分析，转换为

    postagger = Postagger()  # 初始化实例
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger.load(pos_model_path)  # 加载模型

    parser = Parser()  # 初始化实例
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
    parser.load(par_model_path)  # 加载模型

    postags = postagger.postag(resultwordlist)  # 词性标注''
    poslist = []
    for i in postags:
        poslist.append(str(i))
    print(poslist)

    arcs = parser.parse(resultwordlist, poslist)

    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    arcshead = []
    arcsrela = []
    for i in arcs:
        arcshead.append(i.head)
        arcsrela.append(i.relation)
    print(arcshead)
    print(arcsrela)
    semanticlist = []
    length = len(resultwordlist)
    poedictlist = []
    quenum = -1
    for i in range(0, len(resultposlist)):
        if resultposlist[i] == "question":
            quenum = i
    print("resultposlist,resultwordlist:    ", resultwordlist, resultposlist)
    for i in range(0, length):
        if resultposlist[i] in nertypelist:
            num = findproperty(i, arcshead, arcsrela, resultposlist)
            if num != -1:
                # resultposlist[arcshead[i]-1]=="property":#战狼2的上映日期是什么时候 mov的属性是
                # if arcsrela[i]=="ATT" or arcsrela[i]=="SBV":
                poedict = {}
                poedict["headnode"] = resultwordlist[i]
                poedict["headnodetype"] = resultposlist[i]
                if quenum == -1:
                    questr = ""
                else:
                    questr = questiondict[resultwordlist[quenum]]
                properresult = getrelation(propertydict[resultwordlist[num]], resultposlist[i], questr)
                endnodetype = getnodetype(propertydict[resultwordlist[num]], resultposlist[i], questr)
                poedict["relation"] = properresult
                poedict["endnode"] = ""
                poedict["endnodetype"] = endnodetype
                poedict["quesion"] = questr
                poedictlist.append(poedict)
    print(poedictlist)

    postagger.release()  # 释放模型
    parser.release()  # 释放模型
    return poedictlist


def getrelation(property, nodetype, questiontype):  # 桥接操作
    if (property == "verseNextTo" or property == "verseBeforeTo") and nodetype == "VER":
        return property


def getnodetype(property, nodetype, questiontype):
    nodetypeget = ""
    if (property == "verseNextTo" or property == "verseBeforeTo") and nodetype == "VER":
        nodetypeget = nodetype
        return nodetypeget
