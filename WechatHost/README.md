# WechatHost
2022-10-06 微信测试号后台

用于接入微信测试号
在代码运行的状态下，微信测试号收到消息时，会回复相同的消息

1.微信测试号申请<br>
  https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login<br>
  接口配置信息，URL填写程序运行地址（本程序中为使用natapp穿透后的网址）<br>
  TOKEN随便填写，与程序对应即可<br><br>
2.main.py<br>
  对应接口配置信息的后半段<br><br>
3.handle.py<br>
  定义GET和POST两种方法<br>
  GET：微信绑定时验证，同时用于判断是否是微信消息，微信后台会发送signature、timestamp、nonce、echostr<br>
    将TOKEN、imestamp、nonce按字符串排序后组合，再使用sha1加密，与signature比较<br>
    如果验证通过，返回echostr<br>
  POST：使用xml格式接收用户消息，之后再用xml格式回复用户<br>
  接收到的消息，存放到log.txt中<br><br>
4.GenXml.py<br>
  使用xml.dom.minidom插件生成对应的xml消息<br>
