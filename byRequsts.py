import requests
from bs4 import BeautifulSoup
import re
import os


def IdAndPasswd():
    ispList = ["@cmcc", "@unicom", "@telecom"]
    try:
        f = open(".logindata.data", 'r')
        info = []
        for a in f.readlines():
            info.append(a.rstrip('\n'))
        f.close()
        if info.__len__() < 3:
            os.remove(".logindata.data")
            info.append(str(input("输入学号：")))
            info.append(str(input("输入密码：")))
            print("1:中国移动  2:中国联通  3:中国电信")
            number = int(input("选择运营商(1-3)："))
            info.append(ispList[number-1])
            f = open(".logindata.data", 'w')
            f.write("\n".join(info))
            f.close()
    except:
        info = []
        info.append(str(input("输入学号：")))
        info.append(str(input("输入密码：")))
        print("1:中国移动  2:中国联通  3:中国电信")
        number = int(input("选择运营商(1-3)："))
        info.append(ispList[number-1])
        f = open(".logindata.data", 'w')
        f.write("\n".join(info))
        f.close()
    return info


def GetIp():
    HOST = "http://172.16.2.100/"
    r = requests.get(HOST)
    bsobj = BeautifulSoup(r.content, 'html5lib')
    myIp = re.findall(r"ss5=\"(.+?)\"", str(bsobj))[0]
    return myIp


def TestLog(requestObj):
    print("************** test log start *******************")
    print("Status Code: ", end="\t")
    print(requestObj.status_code)
    print("Url: ", end="\t")
    print(requestObj.url)
    print("Headers: ", end="\t")
    print(requestObj.headers)
    print("Cookies: ", end="\t")
    print(requestObj.cookies)
    print("History: ", end="\t")
    print(requestObj.history)
    print("-------------- All content ----------------------")
    print(requestObj.text)
    print("*************** test log end ********************")


def showLog(requestObj):
    result = re.findall(r"认证成功页", requestObj.text)
    if(len(result) > 0):
        for a in range(10):
            print("*************** ok ********************")


def ACLogin(ip, id, passwd, isp):
    url = "http://172.16.2.100:801/eportal/"
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3759.4 Safari/537.36"
    headers["Referer"] = "http://172.16.2.100/a70.htm?wlanuserip="+ip + \
        "&wlanacip=null&wlanacname=null&vlanid=0&ip="+ip + \
        "&ssid=null&areaID=null&mac=00-00-00-00-00-00"
    headers["Connection"] = "keep-alive"
    headers["Host"] = "172.16.2.100:801"
    headers["Origin"] = "http://172.16.2.100"
    payload = {
        "c": "ACSetting",
        "a": "Login",
        "protocol": "http:",
        "hostname": "172.16.2.100",
        "iTermType": "1",
        "wlanuserip": ip,
        "wlanacip": "null",
        "wlanacname": "null",
        "mac": "00-00-00-00-00-00",
        "ip": ip,
        "enAdvert": "0",
        "queryACIP": "0",
        "loginMethod": "1"
    }
    postData = {
        "DDDDD": ",0,"+id+isp,
        "upass": passwd,
        "R1": "0",
        "R2": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "0MKKey": "123456",
        "buttonClicked": "",
        "redirect_url": "",
        "err_flag": "",
        "username": "",
        "password": "",
        "user": "",
        "cmd": "",
        "Login": ""
    }
    cookiesData = {
        "ISP_select": isp,
        "areaID": "null",
        "ip": ip,
        "md5_login2": "%2C0%2C"+id+isp+"%7C"+passwd,
        "program": "test",
        "ssid": "null",
        "vlan": "0"
    }
    acRequest = requests.post(
        url, params=payload, data=postData, cookies=cookiesData, headers=headers)
    showLog(acRequest)


def getIpandMac():
    ipmac = os.popen("ipconfig /all").read()
    ip = re.findall(r"\d+.\d+.\d+.\d+", ipmac)[0]
    mac = re.findall(r"\w+-\w+-\w+-\w+-+\w+-\w+", ipmac)[0]
    dmac = ""
    for a in mac.split("-"):
        dmac += a
    return (ip, dmac,)


def ACLogout(id, passwd, isp):
    ip = getIpandMac()[0]
    mac = getIpandMac()[1]

    url = "http://172.16.2.100:801/eportal/"
    headers = {}
    headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3759.4 Safari/537.36"
    headers["Referer"] = "http://172.16.2.100/a70.htm?wlanuserip="+ip + \
        "&wlanacip=null&wlanacname=null&vlanid=0&ip="+ip + \
        "&ssid=null&areaID=null&mac=00-00-00-00-00-00"
    headers["Connection"] = "keep-alive"
    headers["Host"] = "172.16.2.100:801"
    headers["Origin"] = "http://172.16.2.100"
    payload = {
        "c": "ACSetting",
        "a": "Logout",
        # "protocol": "http:",
        "hostname": "172.16.2.100",
        "iTermType": "1",
        "wlanuserip": "null",
        "wlanacip": "null",
        "wlanacname": "null",
        "mac": mac,
        "queryACIP": "0",
        "port": ""
    }

    cookiesData = {
        "ISP_select": isp,
        "areaID": "null",
        "ip": ip,
        "md5_login2": "%2C0%2C"+id+isp+"%7C"+passwd,
        "program": "test",
        "ssid": "null",
        "vlan": "0"
    }
    acRequest = requests.post(
        url, params=payload, cookies=cookiesData, headers=headers)
    # TestLog(acRequest)


info = IdAndPasswd()
ACLogout(info[0], info[1], info[2])
ip = GetIp()
ACLogin(ip, info[0], info[1], info[2])
