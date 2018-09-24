import requests
import time
import sys
import patient 
account=patient.account
patiendId=patient.account
dutyDate=patient.dutyDate
dpartid=patient.dpartid
hospitalId=patient.hospitalId
cookies = {
}

headers = {
    'Origin': 'http://www.bjguahao.gov.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://www.bjguahao.gov.cn/index.htm',
    'X-Requested-With': 'XMLHttpRequest', 'Proxy-Connection': 'keep-alive',
}

r = requests.post('http://www.bjguahao.gov.cn/quicklogin.htm', headers=headers, cookies=cookies, data=account)
jar = r.cookies
print "login response cookies is : "
print jar

#http://www.bjguahao.gov.cn/dpt/appoint/142-200039584.htm
def sendorder(hos, dep, doc, duty, jar):
    #http://www.bjguahao.gov.cn/order/confirm/225-200003588-200656911-54996394.htm
    refersendorder='http://www.bjguahao.gov.cn/order/confirm/' + hos + '-' + dep + '-' + doc + '-' + str(duty) + ".htm"
    sendorderheader= {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,lb;q=0.6,zh-TW;q=0.5',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.bjguahao.gov.cn',
        'Origin': 'http://www.bjguahao.gov.cn',
        'Referer':refersendorder,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.post('http://www.bjguahao.gov.cn/v/sendorder.htm', headers=sendorderheader, cookies=jar)
    print "send code respose is :"
    print "referer code is " + refersendorder
    print r.content
    code = raw_input("input the verfiy code")
    #code=code.rstrip()

    sendorderheader['Content-Length']='202'
    data = {
        'dutySourceId': duty,
        'hospitalId': hos,
        'departmentId': dep,
        'doctorId': doc,
        'patientId': patientId,
        'hospitalCardId' : '' ,
        'medicareCardId' : '' ,
        'reimbursementType': '10',	#zifei
        'smsVerifyCode': code,
        'childrenBirthday': '',
        'isAjax': 'true'
   }
    r=requests.post('http://www.bjguahao.gov.cn/order/confirm.htm', headers=sendorderheader, cookies=jar, data=data)
    print "order confirmed, reponse is: "
    print r.content
 

dutyTime = ['1', '2']
for date in dutyDate:
    for t in dutyTime:
        data = {
          'hospitalId': hospitalId,
          'departmentId': dpartid,
          'dutyCode': t,
          'dutyDate': date,
          'isAjax': 'true'
        }
        r = requests.post('http://www.bjguahao.gov.cn/dpt/partduty.htm', headers=headers, cookies=jar, data=data)
        #print r.content
        doctorList = r.json()['data']
       # print "Date is : " + str(date) + "time is :" + str(t)
       # print "doctorList"
       # print doctorList

        for doctor in doctorList:
            doctorId = doctor[u'doctorId']
            free=doctor[u'remainAvailableNumber']
            dutysourceId = doctor[u'dutySourceId']
            dutySourceStatus = doctor[u'dutySourceStatus']
            #print "doctor id is  "
            #print doctorId
            #print "free is : "
            #print free
            #print "dutySourceStatus is "
            #print dutySourceStatus

            if free > 0 and dutySourceStatus == 1 :
                print "doctor id is  "
                print doctorId
                print "free is : "
                print free
                time.sleep(1)
                sendorder(hospitalId, dpartid, doctorId, dutysourceId, jar)
                sys.exit(0)

