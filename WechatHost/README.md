# WechatHost
2022-10-06 微信测试号后台

用于接入微信测试号
在代码运行的状态下，微信测试号收到消息时，会回复相同的消息

1.微信测试号申请
  https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
  接口配置信息，URL填写程序运行地址（本程序中为使用natapp穿透后的网址）
  TOKEN随便填写，与程序对应即可
2.main.py
  对应接口配置信息的后半段
3.handle.py
  定义GET和POST两种方法
  GET：微信绑定时验证，同时用于判断是否是微信消息，微信后台会发送signature、timestamp、nonce、
    将TOKEN、imestamp、nonce按字符串排序后组合，再使用sha1加密，与signature比较
    如果验证通过，返回echostr
  POST：使用xml格式接收用户消息，之后再用xml格式回复用户
  接收到的消息，存放到log.txt中
4.GenXml.py
  使用xml.dom.minidom插件生成对应的xml消息
