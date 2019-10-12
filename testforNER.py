# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:52:08 2019

@author: Administrator
"""
from main import evaluate_line,rela
from demo import test,lookfordict,VER

def NER(words):
    entity_name,entity_type,entity_loaction = [],[],[]
    entities_name,entities_type,entities_location = [],[],[]
    result = evaluate_line(words)
    for i in range(len(result['entities'])):
                entity_name = result['entities'][i]['word']
                entity_start_loction = result['entities'][i]['start']
                entity_end_loction = result['entities'][i]['end']
                entity_type = result['entities'][i]['type']
                entities_name.append(entity_name)
                entities_type.append(entity_type) 
                entities_location.append({entity_start_loction,entity_end_loction}) 
                a=''
                t=0
                if result['entities'][i]['type'] == 'VER':
                    a = result['entities'][i]['word']
                    t,eachline = VER(a)
                    if t==1:
                        result['entities'][i]['simlity']=['Find']
                    if t==2:
                        result['entities'][i]['simlity']=[eachline]
                    if t==0:
                        result['entities'][i]['simlity']=['Lost']
    #                        print('VER entity:')
    #                        print(ver)
    
                else:
                    simility=[]
                    a = result['entities'][i]['word']
    #                        print('Normal entity:')
    #                        print(ner)
                    t=lookfordict(a)
                    if t==1:
                        result['entities'][i]['simlity']=['Find']
                    if t==2:
                        #print('Looking up Pinyin....'+a)
                        word = a
                        pyy,t = test(word)
                        if t==3:
                            #print('Lost')
                            result['entities'][i]['simlity']=['Lost']
                        elif t==4:
                            simility.append(pyy)
                            result['entities'][i]['simlity']=[simility]
    return entities_name,entities_type,entities_location
