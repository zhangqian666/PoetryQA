# -*- coding:utf-8 -*-
import re

sentence=u'请从以下十二个字中识别一句七言唐诗：“见，长，安，愁，烟，使，波，人，上 ，未，江，是”'

firstlist=sentence.split("“")
print (firstlist[1])
secondlist=firstlist[1].split("”")
print (secondlist[0])
allwordstring=secondlist[0]
allwordstring=allwordstring.replace(" ","")
print(allwordstring[1])
allwordlist=[]
if "，" in allwordstring:
    allwordlist=allwordstring.split("，")
else:
    for i in range(0,len(allwordstring)):
        allwordlist.append(allwordstring[i])
print (allwordlist)
# matchObj = re.match(r'“(.*?)”', sentence)
# if matchObj:
#     print(matchObj.group(1))