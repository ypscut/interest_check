#encoding:utf-8

from bs4 import BeautifulSoup
import re
import requests
import  time




headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

pattern_89=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(食品|菜|食物|美食))')
pattern_90=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(人|人物|演员|歌手|企业家))')
pattern_91=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(歌曲|音乐|专辑|曲艺))')
pattern_92=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(书|小说|作品|文学))')
pattern_00=re.compile(ur'([\u4e00-\u9fa5]{0,5}?(语言|术语))')

columns=["questionID","answerContentDetail","verifyStatus","verifyStatus_"]



def Process_Data(questionID,answerContentDetail):

    global headers
    global pattern_89
    global pattern_90
    global pattern_91
    global pattern_92
    global pattern_00
    verifyStatus=4
    questionID=int(questionID)

    #answerContentDetail='乖，摸摸头'

    answerContentDetail=answerContentDetail.decode("utf8") #解码
    #answerContentDetail = re.sub(u"(⊙o⊙)|[\/\.\!\\\\_,$%^*\"\'\[\]]+|[——！，。？、~@#￥……&（）'(),-.:;<=>?@^_`|}~·×ΔΨγμφ—‘’“””，…′∈′｜℃Ⅲ↑→［∪φ≈──■▲　、。〈〉《》》），」『』【】〔〕︿！＃＄％＆＇（）÷＊＋ξ，－β．／：；＜±λ＝″☆（－［｛＞？＠［－］∧′＿｛－｜｝～±＋￥]+", u"",answerContentDetail)
    #answerContentDetail = re.sub(u"(⊙o⊙)|[\/\.\!\\\\_,$%^*\"\'\[\]]+|[——！，。？、~@#￥……&（）'(),-.:;<=>?@^_`|}~·×ΔΨγμφ—‘’“””，…′∈′｜℃Ⅲ↑→［∪φ≈──■▲　、。〈〉《》》），」『』【】〔〕︿！＃＄％＆＇（）÷＊＋ξ，－β．／：；＜±λ＝″☆（－［｛＞？＠［－］∧′＿｛－｜｝～±＋￥]+", u"",answerContentDetail)
    #answerContentDetail = re.sub(u"\s+", u" ",answerContentDetail)

    answerContentDetail = re.sub(u"(⊙o⊙)|[\/\!\\\\_,$%^*\"\'\[\]]+|[——！。？、~@#￥&（）'()-:;<=>?@^_`|}~×ΔΨγμφ—‘’“””′∈′｜℃Ⅲ↑→［∪φ≈──■▲　、。〈〉《》》）」『』【】〔〕︿！＃＄％＆＇（）÷＊＋ξ－β／：；＜±λ＝″☆（－［｛＞？＠［－］∧′＿｛－｜｝～±＋￥]+", u"",answerContentDetail)
    answerContentDetail = re.sub(u"\s+", u" ",answerContentDetail)
    answerContentDetail.encode("utf8")

    if len(answerContentDetail)>0:
        try:
            root_url1 = 'http://baike.baidu.com/search?word='+answerContentDetail +'&pn=0&rn=0&enc=utf8'
            html1 = requests.get(root_url1, headers=headers)
            html1.encoding = 'utf-8'
            soup1=BeautifulSoup(html1.text, 'html.parser')
            words=soup1.find("a",class_="result-title").get_text().split('_')[0]

            if answerContentDetail ==words:
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
                            verifyStatus=1
                        else:
                            verifyStatus=4

                    elif questionID==1060890:
                        pattern=re.compile(pattern_90)
                        s=pattern.search(label)
                        #s_g=s.group(1)
                        #print label

                        if s:
                            verifyStatus=1
                        else:
                            verifyStatus=4

                    elif questionID==1060891:
                        #print '**************************'
                        pattern=re.compile(pattern_91)
                        s=pattern.search(label)
                        s_g=s.group(1)
                        #print s_g
                        if s:
                            verifyStatus=1
                        else:
                            verifyStatus=4

                    elif questionID==1060892:
                        pattern=re.compile(pattern_92)
                        s=pattern.search(label)
                        s_g=s.group(1)
                        #print s.group(1)
                        if s:
                            verifyStatus=1
                        else:
                            verifyStatus=4

                    elif questionID==1060893:
                        verifyStatus=4
                    else:
                        verifyStatus=4
                else:
                    verifyStatus=4
        except Exception as e:
            verifyStatus=4
    else:
        verifyStatus=4

    return verifyStatus


def run():


    file=open('test_data','r')
    text = file.read()
    answerContentDetails = text.splitlines()
    out=open('out_test','w')
    i=0
    for c in answerContentDetails:
        print 'Process %s data' %i
        List=c.split(',')
        questionID=List[0]
        answerContentDetail=List[1].strip()

        verifyStatus=List[2]
        verifyid_list=List[3]
        verifyStatus_=Process_Data(questionID,answerContentDetail)
        out.write(str(questionID)+','+answerContentDetail+','+str(verifyStatus)+','+str(verifyStatus_)+','+str(verifyid_list))
        out.write('\n')
        i+=1
    out.close()

if __name__=="__main__":

    now = time.time()

    print("please wait..")
    run()
    print("All is done!")
    cost_time = time.time()-now
    print "end ......",'\n',"cost time:",cost_time,"(s)......"
