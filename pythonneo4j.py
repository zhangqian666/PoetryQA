#-*- coding:utf-8 -*-
import os
import jieba.posseg as pseg
from py2neo import Graph,Node,Relationship

test_graph = Graph("http://localhost:7474/browser/",username="neo4j",password="neo4j")
test_graph=test_graph.begin()
find_code_1 = test_graph.run(
    "MATCH(m:Verse{verseContext: \"天台四万八千丈\"})-[: verseBeforeTo]->(b:Verse) return b.verseContext"
)
# find_code_1 = test_graph.find_one(
#   label="People",
#   property_key="peopleName",
#   property_value="李白"
# )
print (find_code_1)

