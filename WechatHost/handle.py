# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import xml.dom.minidom as minixml
from GenXml import toXml
import time

from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            #print(data)
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "zyw" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            str = list[0]+list[1]+list[2]
            #print(str)
            hashcode = hashlib.sha1(str.encode('utf-8')).hexdigest()
            #print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return "hashcode != signature"
        except (Exception, Argument):
            return Argument

    def POST(self):
        getdata = web.data()
        #print(getdata)
        rootNode = minixml.parseString(getdata)
        GetToUser = rootNode.getElementsByTagName("ToUserName")[0].childNodes[0].data
        GetFromUser = rootNode.getElementsByTagName("FromUserName")[0].childNodes[0].data
        GetMsgType = rootNode.getElementsByTagName("MsgType")[0].childNodes[0].data
        if GetMsgType == 'text':
            GetContent = rootNode.getElementsByTagName("Content")[0].childNodes[0].data
            reply = ""
            if GetContent == "你好" or GetContent == "hello":
                reply = "你好，小阅阅"
            else:
                qkyUrls='http://api.qingyunke.com/api.php?key=free&appid=0&msg='+GetContent
                response = requests.get(qkyUrls)
                reply = json.loads(response.content)
                reply = reply['content']
            PostXml = toXml.textXml(GetFromUser,GetToUser,reply)
        elif GetMsgType == 'image':
            GetContent = rootNode.getElementsByTagName("MediaId")[0].childNodes[0].data
            PostXml = toXml.imageXml(GetFromUser,GetToUser,GetContent)
        else:
            GetContent = "未识别的消息"
            PostXml = toXml.textXml(GetFromUser,GetToUser,"你好，该功能尚在维护中")
        #print(PostXml)
        note = open('log.txt','a+')
        note.write('【'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'】\n')
        note.write(GetFromUser+' : '+GetContent+'\n')
        note.write('AutoReply : '+reply+'\n')
        note.close()
        return PostXml
        

