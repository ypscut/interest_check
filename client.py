#encoding:utf-8
import requests
import time
data="{'memberID':'81812345','content':[{'questionID': 1060889, 'answerContentDetail':'糖醋排骨' },{'questionID': 1060890, 'answerContentDetail':'刘德华' },{'questionID': 1060891, 'answerContentDetail':'吻别' },{'questionID': 1060892, 'answerContentDetail':'《水浒传》' },{'questionID': 1060893, 'answerContentDetail':'打篮球' }]}"

data3="{'memberID':'81812345','content':[{'questionID': 1060893, 'answerContentDetail':'打篮球' }]}"



data1="""{"content":[{"answerContentDetail":"糖醋排骨","questionID":1060889},{"answerContentDetail":"克林顿","questionID":1060890},{"answerContentDetail":"下一个天亮","questionID":1060891},{"answerContentDetail":"傲慢与偏见","questionID":1060892}],"memberID":81812116}
"""

data="{'content':[{'answerContentDetail':'','questionID':1060892}],'memberID':81812116}"



now=time.time()
#r = requests.post('http://127.0.0.1:5000/check',data=data)
r = requests.post('http://10.10.9.102:5500/check',data=data)

print "cost time %s s" %(time.time()-now)
print(type(r.text))
print r.text
