import itchat
import re #正则表达式
from snownlp import SnowNLP #自然语言文本处理
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
#爬取好友的相关信息，返回一个json文件

#自动登录微信
itchat.auto_login(hotReload=True)
#获取用户的所有的朋友信息
friends = itchat.get_friends(update=True)
#获取好友的签名
def getSignature():
    #打开一个文件
    with open("sig.txt", "w", encoding="utf-8") as file:
        for f in friends:
            #去除前后空格,去除特殊符
            #signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
            signature = f["Signature"].strip()
            #使用正则表达式提取汉字
            rec = re.compile("[^\u4e00-\u9fa5]")
            signature = rec.sub("", signature)
            if signature:
                #进行情感处理,s是 [0, 1] 之间的小数，数值越大越褒义，越小越消极
                s = SnowNLP(signature)
                if s.sentiments > 0.55:
                    file.write(signature + "\n")
                elif s.sentiments <= 0.55:
                    file.write(signature + "\n")

#生成词云函数
def create_wordcloub(filename):
    #读取文件
    text = open(filename, encoding="utf-8").read()
    #分词，全分词
    wordlist = jieba.cut(text, cut_all=True)
    #使用空格连接分词内容
    wl = " ".join(wordlist)
    coloring = np.array(Image.open("123.png"))
    #设置词云
    wc = WordCloud(background_color="white", max_words=300, font_path="simfang.ttf",height=500,width=500,max_font_size=60,random_state=30, mask=coloring)
    myword=wc.generate(wl)
    plt.imshow(myword)
    # 关闭坐标系
    plt.axis("off")
    plt.show()
    #保存到文件中
    wc.to_file("sign.png")
    #发送给文件助手
    itchat.send_image("sign.png", "filehelper")

getSignature()
create_wordcloub("sig.txt")
