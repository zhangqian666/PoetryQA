#coding=utf-8
import json
import os

import pika

from pyltp import Postagger, Parser

from nermain import NER
from sentence2logistcal import answerrecognition
from sentence2logistcal import answersemantic
from readDict import readPropertyWord
from readDict import readQuestionWord
from py2neo import Graph, Node, Relationship, NodeMatcher  # 读取数据库中内容
from demo import test, lookfordict, VER
from logistical2neo4j import semantic2neo4j
from mixstringforverse import frommixwordfindverse
from readDict import readallverse

direct_exchange = "direct.exchange"
direct_queue1 = "direct.queue1"
direct_queue2 = "direct.queue2"
direct_routing_key1 = "direct.pwl1"
direct_routing_key2 = "direct.pwl2"

verseset = readallverse()
# LTP_DATA_DIR = '/Users/zhangqian/PycharmProjects/pyltp/ltp_data_v3.4.0/'  # ltp模型目录的路径
LTP_DATA_DIR = '/develop/python3/PoetryQA/ltp_data_v3.4.0/'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
parser = Parser()  # 初始化实例
parser.load(par_model_path)  # 加载模型
test_graph = Graph("http://connect-ai.cn:7474", username="neo4j", password="123456")
resultwordlist = []
resultposlist = []
propertywordlist = []
questionwordlist = []

potlist = []
propertylist, propertydict = readPropertyWord()
questionlist, questiondict = readQuestionWord()
print(questiondict)


def question_one(sentence):
    # 第一类纠错字类题目
    entitylist, poslist, indexset = NER(sentence)  # 命名实体识别
    for i in entitylist:
        flag, resultver = VER(i)
        if flag == 2:
            for unitindex in range(0, len(i)):
                if i[unitindex] != resultver[unitindex]:
                    return "“" + i[unitindex] + "”应改为" + "“" + resultver[unitindex] + "”"


def question_two(sentence):
    verseset = readallverse()
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
    return frommixwordfindverse(allwordlist, verseset)


def question_three(sentence):
    entitylist, poslist, indexset = NER(sentence)  # 命名实体识别
    print(entitylist, poslist)
    resultwordlist, resultposlist = answerrecognition(sentence, entitylist, poslist, indexset)
    print(resultwordlist)
    print(resultposlist)
    poedictlist = answersemantic(resultwordlist, resultposlist)
    poedictlist = semantic2neo4j(poedictlist)
    answerentity = poedictlist[0]['endnode'][0]
    return answerentity


def queue_receiver(ch, method, properties, body):
    print("queue1 keu : {1}收到消息:{0}".format(body, method.routing_key))
    body = str(body, "utf-8")

    rbUserBean = json.loads(body, encoding="utf-8")
    questionStr = rbUserBean["question"]

    print("转码过后:{0}".format(questionStr))
    result = "没有结果"
    if "错" in questionStr and "字" in questionStr:
        try:
            result = question_one(questionStr)
        except:
            result = "解析错字问题出现错误"
    elif "识别" in body:
        try:
            result = question_two(questionStr)
        except:
            result = "解析识别问题出现错误"
    elif ("上一句" in body) or ("下一句" in body):
        try:
            result = question_three(questionStr)
        except:
            result = "解析上一句或者下一句问题出现错误"
    else:
        result = "无法识别，请重新输入"

    print("处理完 得到的结果为：{0}".format(result))
    rbUserBean["answer"] = result
    resultStr = json.dumps(rbUserBean, ensure_ascii=False)
    send_answer(resultStr)


def send_answer(answer):
    connection = pika.BlockingConnection(pika.ConnectionParameters("connect-ai.cn", 5672))
    channel = connection.channel()

    channel.exchange_declare(exchange=direct_exchange,
                             exchange_type='direct',
                             durable=True)

    channel.basic_publish(exchange=direct_exchange,
                          routing_key=direct_routing_key2,
                          body=answer)
    channel.close()


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters("connect-ai.cn", 5672))
    channel = connection.channel()

    channel.exchange_declare(exchange=direct_exchange,
                             exchange_type='direct',
                             durable=True)

    channel.queue_bind(exchange=direct_exchange,  # queue绑定到转发器上
                       queue=direct_queue1,
                       routing_key=direct_routing_key1)

    channel.basic_consume(on_message_callback=queue_receiver, queue=direct_queue1, auto_ack=True)
    channel.start_consuming()
