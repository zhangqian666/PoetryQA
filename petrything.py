# -*- coding:utf-8 -*-

from nermain import NER
from nermain import build_model
from sentence2logistcal import answerrecognition
from sentence2logistcal import answersemantic
from demo import VER
from logistical2neo4j import semantic2neo4j
from mixstringforverse import frommixwordfindverse
from readDict import readallverse
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
model = None

if __name__ == "__main__":


    # 第一类问题 上一句下一句
    sentence = "“开国何茫然”的前一句是什么？"  # 黄河之水天上来的下一句是？,verlist有的诗句都可以回答下一句，上一句，前一句，后一句
    # sentence = "“黄河之水天上来”的下一句是什么？"
    # 第二类问题 纠错字类
    # sentence = "请问“穷年忧犁元，叹息肠内热”中哪个字是错误的？"  # 任何一句诗句中的哪个字是错误的问题，需要问题中包含错和字两个关键字
    # sentence = "“白头搔更短，混欲不胜簪。”中的那个字是错的？"
    # 第三类问题 乱序字符串中识别
    # sentence = "请从以下十二个字中识别一句七言唐诗：“见，长，安，愁，烟，使，波，人，上 ，未，江，是”"
    # sentence = "123"
    # sentence = "请从以下九个字中识别一句五言唐诗：“花，多，又，知，多，时，雨，少，落”"
    while True:
        if "错" in sentence and "字" in sentence:
            # 第一类纠错字类题目
            entitylist, poslist, indexset = NER(sentence)  # 命名实体识别
            for i in entitylist:
                flag, resultver = VER(i)
                if flag == 2:
                    for unitindex in range(0, len(i)):
                        if i[unitindex] != resultver[unitindex]:
                            print("“" + i[unitindex] + "”应改为" + "“" + resultver[unitindex] + "”")
        elif "识别" in sentence:
            firstlist = sentence.split("“")
            secondlist = firstlist[1].split("”")
            allwordstring = secondlist[0]
            allwordstring = allwordstring.replace(" ", "")
            allwordlist = []
            if "，" in allwordstring:
                allwordlist = allwordstring.split("，")
            else:
                for i in range(0, len(allwordstring)):
                    allwordlist.append(allwordstring[i])

            verseset = readallverse()
            frommixwordfindverse(allwordlist, verseset)
        else:
            entitylist, poslist, indexset = NER(sentence)  # 命名实体识别
            print(entitylist, poslist,indexset)
            resultwordlist, resultposlist = answerrecognition(sentence, entitylist, poslist, indexset)
            print("resultwordlist,resultposlist:    ", resultwordlist, resultposlist)
            poedictlist = answersemantic(resultwordlist, resultposlist)
            poedictlist = semantic2neo4j(poedictlist)
            answerentity = poedictlist[0]['endnode'][0]
            print(answerentity)
