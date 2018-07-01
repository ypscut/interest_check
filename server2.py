#encoding:utf-8

from flask import Flask, request
from bs4 import BeautifulSoup
import re
import requests

server = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}


pattern_89=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(食品|菜|食物|美食))')
pattern_90=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(人|人物|演员|歌手|企业家))')
pattern_91=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(歌曲|音乐|专辑))')
pattern_92=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(书|小说|文学|作品))')

pattern_00=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(语言|术语))')



def Process_Data(questionID,answerContentDetail):

    global headers
    global pattern_89
    global pattern_90
    global pattern_91
    global pattern_92
    global pattern_00
    answerContentDetail = answerContentDetail.decode("utf8")
    #answerContentDetail = re.sub(u"(⊙o⊙)|[\/\.\!\\\\_,$%^*\"\'\[\]]+|[——！，。？、~@#￥……&（）'(),-.:;<=>?@^_`|}~·×ΔΨγμφ—‘’“””，…′∈′｜℃Ⅲ↑→［∪φ≈──■▲　、。〈〉《》》），」『』【】〔〕︿！＃＄％＆＇（）÷＊＋ξ，－β．／：；＜±λ＝″☆（－［｛＞？＠［－］∧′＿｛－｜｝～±＋￥]+", u"",answerContentDetail)

    answerContentDetail = re.sub(u"(⊙o⊙)|[\/\!\\\\_,$%^*\"\'\[\]]+|[——！。？、~@#￥……&（）'()-:;<=>?@^_`|}~·×ΔΨγμφ—‘’“””…′∈′｜℃Ⅲ↑→［∪φ≈──■▲　、。〈〉《》》）」『』【】〔〕︿！＃＄％＆＇（）÷＊＋ξ－β．／：；＜±λ＝″☆（－［｛＞？＠［－］∧′＿｛－｜｝～±＋￥]+", u"",answerContentDetail)
    answerContentDetail = re.sub(u"\s+", u" ",answerContentDetail)
    answerContentDetail.encode("utf8")

    if len(answerContentDetail)>0:
        try:
            root_url1 = 'http://baike.baidu.com/search?word='+answerContentDetail +'&pn=0&rn=0&enc=utf8'
            html1 = requests.get(root_url1, headers=headers)
            html1.encoding = 'utf-8'
            soup1=BeautifulSoup(html1.text, 'html.parser')
            words=soup1.find("a",class_="result-title").get_text().split('_')[0]

            if answerContentDetail==words:
                href=soup1.find("a",class_="result-title").get('href')
                #print root_url
                html = requests.get(href, headers=headers)
                html.encoding = 'utf-8'

                soup = BeautifulSoup(html.text, 'html.parser')
                label=soup.find_all(id="open-tag-item")[0].get_text()

                pattern00=re.compile(pattern_00)
                s=pattern00.search(label)
                if not s:
                    if questionID==1060889:                     # 最喜欢的一道菜

                        pattern=re.compile(pattern_89)
                        s=pattern.search(label)
                        #print s.group(1)
                        if s:
                            #print "成功啦！！！！！！！！！！！！！！！！！！！！！！！！"
                            return {"questionID":questionID,"verifyStatus":1,"verifyMsg":"xxx"}
                        else:
                            return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}


                    elif questionID==1060890:
                        pattern=re.compile(pattern_90)
                        s=pattern.search(label)
                        #print s.group(1)
                        #print label
                        #print questionID," + ",s
                        if s:
                            return {"questionID":questionID,"verifyStatus":1,"verifyMsg":"xxx"}
                        else:
                            return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}

                    elif questionID==1060891:
                        pattern=re.compile(pattern_91)
                        s=pattern.search(label)
                        #print s.group(1)
                        if s:
                            return {"questionID":questionID,"verifyStatus":1,"verifyMsg":"xxx"}
                        else:
                            return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}

                    elif questionID==1060892:
                        pattern=re.compile(pattern_92)
                        s=pattern.search(label)
                        #print s.group(1)
                        if s:
                            return {"questionID":questionID,"verifyStatus":1,"verifyMsg":"xxx"}
                        else:
                            return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}

                    elif questionID==1060893:
                        return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}
                else:
                    return  {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}
            else:
                verifyStatus=4

                return {"questionID":questionID,"verifyStatus":verifyStatus,"verifyMsg":"xxx"}

        except Exception as e:
            return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}
    else:
        return {"questionID":questionID,"verifyStatus":4,"verifyMsg":"xxx"}






@server.route('/check', methods=['POST'])
def register():
    #print(request.data)
    recvdata = eval(request.data)
    memberid = recvdata['memberID']
    contents=recvdata['content']   #列表
    result_contents=[]
    for content in contents:
        #a=content
        result_contents.append(Process_Data(content['questionID'],content['answerContentDetail']))

    return str({"status":1,"memberID":memberid,"content":result_contents})



if __name__ == '__main__':
    #server.run(host='10.10.9.102',port=int('5500'),debug=True)
    server.run(host='127.0.0.1',port=int('5000'),debug=True)