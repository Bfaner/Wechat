import xml.dom.minidom as minixml
import time

class toXml():
        def textXml(toUser,fromUser,Content):
                impl = minixml.getDOMImplementation()
                domTree = impl.createDocument(None, 'xml', None)
                rootNode = domTree.documentElement
                #新建节点-to
                toUserNode = domTree.createElement("ToUserName")
                toUserNodeTxt = domTree.createCDATASection(toUser)
                toUserNode.appendChild(toUserNodeTxt)
                #新建节点-from
                fromUserNode = domTree.createElement("FromUserName")
                fromUserNodeTxt = domTree.createCDATASection(fromUser)
                fromUserNode.appendChild(fromUserNodeTxt)
                #新建节点-time
                createtimeNode = domTree.createElement("CreateTime")
                createtimeNodeTxt = domTree.createTextNode(str(int(time.time())))
                createtimeNode.appendChild(createtimeNodeTxt)
                #新建节点-type
                TypeNode = domTree.createElement("MsgType")
                TypeNodeTxt = domTree.createCDATASection("text")
                TypeNode.appendChild(TypeNodeTxt)
                #新建节点-content
                contentNode = domTree.createElement("Content")
                if Content == "你好" or Content == "hello":
                    contentNodeTxt = domTree.createCDATASection("你好，小阅阅")
                else:
                    contentNodeTxt = domTree.createCDATASection(Content)
                contentNode.appendChild(contentNodeTxt)
                #加入根节点中
                rootNode.appendChild(toUserNode)
                rootNode.appendChild(fromUserNode)
                rootNode.appendChild(createtimeNode)
                rootNode.appendChild(TypeNode)
                rootNode.appendChild(contentNode)
                return domTree.toxml('utf-8').decode('utf-8')

        def imageXml(toUser,fromUser,PicUrl):
                impl = minixml.getDOMImplementation()
                domTree = impl.createDocument(None, 'xml', None)
                rootNode = domTree.documentElement
                #新建节点-to
                toUserNode = domTree.createElement("ToUserName")
                toUserNodeTxt = domTree.createCDATASection(toUser)
                toUserNode.appendChild(toUserNodeTxt)
                #新建节点-from
                fromUserNode = domTree.createElement("FromUserName")
                fromUserNodeTxt = domTree.createCDATASection(fromUser)
                fromUserNode.appendChild(fromUserNodeTxt)
                #新建节点-time
                createtimeNode = domTree.createElement("CreateTime")
                createtimeNodeTxt = domTree.createTextNode(str(int(time.time())))
                createtimeNode.appendChild(createtimeNodeTxt)
                #新建节点-type
                TypeNode = domTree.createElement("MsgType")
                TypeNodeTxt = domTree.createCDATASection("image")
                TypeNode.appendChild(TypeNodeTxt)
                #新建节点-Image大节点
                imageNode = domTree.createElement("Image")
                #新建节点-content
                picNode = domTree.createElement("MediaId")
                picNodeTxt = domTree.createCDATASection(PicUrl)
                picNode.appendChild(picNodeTxt)
                imageNode.appendChild(picNode)
                #加入根节点
                rootNode.appendChild(toUserNode)
                rootNode.appendChild(fromUserNode)
                rootNode.appendChild(createtimeNode)
                rootNode.appendChild(TypeNode)
                rootNode.appendChild(imageNode)
                return domTree.toxml('utf-8').decode('utf-8')
