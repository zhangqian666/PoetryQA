f = open("pinyin2word.model.dump","r",encoding='utf8')#二进制格式读文件
line = f.readline()
print(type(line))
##if not line:
##    break
##else:
##    try:
##        print(line.decode('utf8'))
##        line.decode('utf8')
##            #为了暴露出错误，最好此处不print
##    except:
##        print(str(line))
