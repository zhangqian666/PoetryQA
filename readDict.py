# -*- coding: utf-8 -*-

import os
def readallverse():
	f = open('qadata/allverse.txt', 'r', encoding='utf8')
	lines=f.readlines()
	lineset=set()
	for i in lines:
		i=i.replace("\n","")
		lineset.add(i)
	return lineset
def readPropertyWord():
	f=open('qadata/poetry','r',encoding='utf8')
	lines=f.read().split("\n")
	prolist=[]
	prodict={}
	for i in lines:
		units=i.split(" ")
		for j in range(0,len(units)):
			if j==0:
				continue
			units[j]=units[j].replace(" ","")
			if units[j]!="":
				prolist.append(units[j])
				prodict[units[j]]=units[0]
	return prolist,prodict

def readQuestionWord():
	f = open('qadata/question_word_poetry', 'r',encoding='utf8')
	lines=f.read().split("\n")
	prolist=[]
	prodict={}
	for i in lines:
		units=i.split(" ")
		for j in range(0,len(units)):
			if j==0:
				units[j]=units[j].replace(" ","")
				continue
			units[j]=units[j].replace(" ","")
			if units[j]!="":
				prolist.append(units[j])
				prodict[units[j]]=units[0]
	return prolist,prodict

def writeWord():
	oneword=[]
	twoword=[]
	threeword=[]
	fourword=[]
	fiveword=[]
	sixword=[]
	f=open('E:/ENN/myDjango/projectApp/question_word.txt','r')
	lines=f.read().split("\n")
	prolist=[]
	for i in lines:
		units=i.split(" ")
		for j in range(0,len(units)):
			if j==0:
				continue
			units[j]=units[j].replace(" ","")
			if units[j]!="":
				if len(units[j])==3:
					oneword.append(units[j])
				elif len(units[j])==6:
					twoword.append(units[j])
				elif len(units[j])==9:
					threeword.append(units[j])
				elif len(units[j])==12:
					fourword.append(units[j])
				elif len(units[j])==15:
					fiveword.append(units[j])
				elif len(units[j])==18:
					sixword.append(units[j])
	f.close()
	f=open('./film.txt','r')
	lines=f.read().split("\n")
	for i in lines:
		units=i.split(" ")
		for j in range(0,len(units)):
			if j==0:
				continue
			units[j]=units[j].replace(" ","")
			if units[j]!="":
				if len(units[j])==3:
					oneword.append(units[j])
				elif len(units[j])==6:
					twoword.append(units[j])
				elif len(units[j])==9:
					threeword.append(units[j])
				elif len(units[j])==12:
					fourword.append(units[j])
				elif len(units[j])==15:
					fiveword.append(units[j])
				elif len(units[j])==18:
					sixword.append(units[j])
	f.close()
	f=open('E:\oneword.txt','w')
	for i in oneword:
		f.write(str(i)+' '+'50'+'\n')
	f.close()
	f=open('E:\secondword.txt','w')
	for i in twoword:
		f.write(str(i)+' '+'100'+'\n')
	f.close()	
	f=open('E:\sthreeword.txt','w')
	for i in threeword:
		f.write(str(i)+' '+'150'+'\n')
	f.close()	
	f=open('E:\sfourword.txt','w')
	for i in fourword:
		f.write(str(i)+' '+'200'+'\n')
	f.close()
	f=open('E:\sfiveword.txt','w')
	for i in fiveword:
		f.write(str(i)+' '+'250'+'\n')
	f.close()
	f=open('E:\sixword.txt','w')
	for i in sixword:
		f.write(str(i)+' '+'300'+'\n')
	f.close()

    # quelist,quedict=readQuestionWord()
    # print len(prolist)
    # print prodict["票房"]
    # print quedict["什么时候"]
    # writeWord()
	
