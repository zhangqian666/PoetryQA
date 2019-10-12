import sys
import os
import jieba
from pyltp import *

address= "高大城墙上有百尺高的城楼，在绿杨林子外是水中的沙洲，年少有为的贾谊徒然地流泪，春日登楼的王粲再度去远游，常向往老年自在地归隐江湖，要想在扭转乾坤后逍遥扁舟，不知道腐臭的死鼠成了美味，竟对鹓雏的爱好也猜忌不休。"
words=[]
seg_list=jieba.cut(address)
for i in seg_list:
    words.append(i)

postagger = Postagger()
postagger.load("E:\\ltp_data\\pos.model")
postags = postagger.postag(words)

recognizer = NamedEntityRecognizer()
recognizer.load("E:\\ltp_data\\ner.model")
netags = recognizer.recognize(words, postags)

for word,postag,netag in zip(words,postags,netags):
    print(word+'/'+postag+'/'+netag)