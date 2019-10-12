# -*- coding:utf-8 -*-
import os
import jieba.posseg as pseg
from py2neo import Graph
from pyltp import Postagger
from pyltp import Parser
from nermain import NER
import jieba.posseg as pseg
import jieba
from readDict import readPropertyWord
from readDict import readQuestionWord

jieba.load_userdict('qadata/userdict.txt')

from py2neo import Graph, Node, Relationship
from pyltp import Postagger
from pyltp import Parser
LTP_DATA_DIR = '/Users/zhangqian/PycharmProjects/pyltp/ltp_data_v3.4.0/'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
parser = Parser()  # 初始化实例
parser.load(par_model_path)  # 加载模型
propertylist, propertydict = readPropertyWord()#读取关系词，并做成词典
questionlist, questiondict = readQuestionWord()#读取问题词，并做成词典
nertypelist=['VER','POT']
def answerrecognition(sentence,entitylist,poslist,indexset):#命名实体识别、抽取句子中的关系词、问题词
    indexlist = []#取出indexset中较小的值，组成indexlist
    for index in indexset:
        smallnum = 1000
        for i in index:
            if i < smallnum:
                smallnum = i
        indexlist.append(smallnum)
    allwordlist = entitylist
    allposlist = poslist
    allweilist = indexlist
    resultwordlist=[]
    resultposlist=[]
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

    return resultwordlist,resultposlist
def findproperty(i, arcshead, arcsrela, resultposlist):#寻找属性词
    if resultposlist[i] != "property" and arcshead[i] - 1 >= 0:
        i = arcshead[i] - 1
        return findproperty(i, arcshead, arcsrela, resultposlist)
    elif resultposlist[i] != "property" and arcshead[i] - 1 < 0:
        return -1
    else:
        return i
# def findnerandproperty(i,arcshead,arcsrela,resultposlist,resultwordlist):
#     headnodelist=[]
#     headnodetypelist=[]
#     propertylist=[]
#     questionlist=[]
#     for k in range(0, len(arcshead)):
#         if arcshead[k] - 1 == i and arcsrela[k] == "ATT":
#             if resultposlist[k] in nertypelist:
#                 headnodelist.append(resultwordlist[k])
#                 headnodetypelist.append(resultwordlist[k])
#                 propertylist.append(resultwordlist[i])
#             elif resultposlist[k] == "property":
#                 headlist,headtypelist,prolist,quelist=findnerandproperty(k,arcshead,arcsrela,resultposlist,resultwordlist)
#                 headnodelist=headlist+headnodelist
#                 headnodetypelist=headtypelist+headnodetypelist
#                 propertylist=prolist+propertylist
#                 questionlist=quelist+questionlist
#             elif resultposlist[k]=="question":
#                 questionlist.append(resultwordlist[k])
#     return headnodelist,headnodetypelist,propertylist,questionlist
#
# def findsentencestructure(arcshead,arcsrela,resultposlist,resultwordlist):
#     for k in range(0, len(arcsrela)):
#         if arcsrela[k] == "HED":
#             hed = k
#     headnodelist=[]
#     headnodetypelist=[]
#     propertylist=[]
#     endnodelist=[]
#     endnodetypelist=[]
#     questionlist=[]
#     judgeobject=0
#     for i in range(0,len(arcsrela)):
#         if arcshead[i] - 1 == hed:
#             if arcsrela[i] == "SBV":#判断成分缺失和多跳
#                 if resultposlist[i] =="property":
#                     headnodelist,headnodetypelist,propertylist,questionlist=findnerandproperty(i,arcshead,arcsrela,resultposlist,resultwordlist)
#                 elif resultposlist[i] in nertypelist:
#                     headnodelist.append(resultwordlist[i])
#                     headnodetypelist.append(resultposlist[i])
#                 elif resultposlist[i]=="question":
#                     questionlist.append(resultwordlist[i])
#                 if len(questionlist)>0:
#                     judgeobject=1 #该标号为标志符，为1则




    #         for j in range(0, len(arcshead)):
    #             if j != i and arcshead[j] - 1 == hed and resultposlist[j] == "property":
    #                 if arcsrela[j] == "SBV" or arcsrela[j] == "VOB":
    #                     flag = True
    #                     flagnum = j
    #         if flag:
    #             return flagnum
    #         else:
    #             return -1
    #     else:
    #         return -1
    # else:
    #     return -1


def findobject(i, arcshead, arcsrela, resultposlist):
    if resultposlist[i] not in nertypelist and arcshead[i] - 1 >= 0:
        i = arcshead[i] - 1
        return findproperty(i, arcshead, arcsrela, resultposlist)
    elif resultposlist[i] not in nertypelist and arcshead[i] - 1 < 0:
        return -1
    else:
        return i
def answersemantic(resultwordlist,resultposlist):#根据ltp进行句法分析，转换为
    postags = postagger.postag(resultwordlist)  # 词性标注''
    poslist = []
    for i in postags:
        poslist.append(str(i))
    print(poslist)
    # postagger.release()  # 释放模型
    arcs = parser.parse(resultwordlist, poslist)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    # parser.release()  # 释放模型
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
                poedict["endnodetype"]=endnodetype
                poedict["quesion"] = questr
                poedictlist.append(poedict)
    print(poedictlist)
    return poedictlist

def getrelation(property, nodetype, questiontype):#桥接操作
    if (property=="verseNextTo" or property=="verseBeforeTo") and nodetype=="VER":
        return property

def getnodetype(property,nodetype,questiontype):
    nodetypeget=""
    if (property=="verseNextTo" or property=="verseBeforeTo") and nodetype=="VER":
        nodetypeget=nodetype
        return nodetypeget