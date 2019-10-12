# -*- coding:utf-8 -*-
import os
from py2neo import Graph, Node, Relationship, NodeMatcher  # 读取数据库中内容

test_graph = Graph("http://connect-ai.cn:7474/browser/",username="neo4j",password="123456")
test_graph=test_graph.begin()
matcher = NodeMatcher(test_graph)
# # print('versename ',versename )
#                 pth = matcher.match("Poetrything", poetrythingName=hd).first()  # 返回的是一个节点
#                 i = pth['poetrythingMeaning']
# find_code_1 = test_graph.run(
#     "MATCH(m:Verse{verseContext: \"天台四万八千丈\"})-[: verseBeforeTo]->(b:Verse) return b.verseContext"
# )
# def getendnodetype(poedict):
#     if poedict["relation"]=="verseNextTo" or "verseBeforeTo":
#         if poedict["endnodetype"]=="":
#             poedict["endnodetype"]=poedict["headn"]
#     return poedict
def aliasalignment(poedict):
    if poedict["headnodetype"]=="VER":
        poedict["headnodetype"]="Verse"
    if poedict["endnodetype"]=="VER":
        poedict["endnodetype"]="Verse"
    return poedict
def getnodename(node):
    if node=="Verse":
        return "verseContext"

def onehopsearch(poedict):
    poedict=aliasalignment(poedict)
    if poedict["relation"]!="":
        if poedict["headnode"]!="":
            hdname = getnodename(poedict["headnodetype"])
            excutepath = "MATCH (m:{headnodetype}{{{headnodename}:\"{headnode}\"}})-[:{relation}]->(b:{endnodetype}) return b".format(
                headnodetype=poedict["headnodetype"], \
                relation=poedict["relation"], headnodename=hdname, headnode=poedict["headnode"],
                endnodetype=poedict["endnodetype"])
            print(excutepath)
            data = test_graph.run(excutepath)
            recordlist = data.data()
            endnode=[]
            endname=getnodename(poedict['endnodetype'])
            for i in recordlist:
                print(i['b'][endname])
                if i['b'][endname] not in endnode:
                    endnode.append(i['b'][endname])
            poedict["endnode"] = endnode

    print (poedict)
    return poedict

def semantic2neo4j(poedictlist):
    for i in range(0,len(poedictlist)):
        poedictlist[i]=onehopsearch(poedictlist[i])
    print(poedictlist)
    return poedictlist

