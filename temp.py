
import Levenshtein as ls
a = input("please input : ")
s=0
with open('mydict',encoding = 'utf8') as f:
    for i in f:
        eachline = i.strip()
       # print('one')
        if a == eachline:
            print('find the word')
            s+=1
       # else:
            #print(ls.distance(a,eachline))
        elif ls.distance(a,eachline) <= 1:
            print('exist similty word')
            print(eachline)
#if s == 0:
    

