# -*- coding:utf-8 -*-
import os
from py2neo import Graph, Node, Relationship, NodeMatcher  # 读取数据库中内容
from py2neo.matching import RelationshipMatcher

test_graph = Graph("http://localhost:7474/browser/",username="neo4j",password="neo4j")
test_graph=test_graph.begin()
matcher = NodeMatcher(test_graph)
endnode = []
# data='打卡时间：{date},打卡人：{name},所在部门：{department}'.format(date=d,name=n,department=dep)
# print(data)
versename="蚕丛及鱼凫"
poedict={}
poedict["relation"]="verseBeforeTo"
poedict["headnodetype"]="Verse"
poedict["headnode"]="蚕丛及鱼凫"
headnodename="verseContext"
poedict["endnodetype"]="Verse"
excutepath = "MATCH (m:{headnodetype}{{{headnodename}:\"{headnode}\"}})-[:{relation}]->(b:{endnodetype}) return b".format(headnodetype=poedict["headnodetype"],\
relation=poedict["relation"],headnodename=headnodename,headnode=poedict["headnode"],endnodetype=poedict["endnodetype"])
print(excutepath)
data = test_graph.run(excutepath)
recordlist = data.data()
for i in recordlist:
    print(i['b']['verseAuthor'])
    endnode.append(i['b']['verseContext'])
poedict["endnode"] = endnode
