from flask import Flask, request, session, g, redirect, url_for, abort, render_template, make_response
import json
from lxml import etree
import time
import logging
import requests
# from . import config
import re
from bs4 import BeautifulSoup

logging.basicConfig(filename='logger.log', level=logging.INFO)

app = Flask(__name__)


# /weixin?signature=b50cb9c0bbf196b3cb3bc8f42b89eeee65a090d0&echostr=457557273493372605&timestamp=1523967673&nonce=1003935488
def do_verify():
    print(request.url)
    signature = request.args.get('signature')
    echostr = request.args.get('echostr')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    
    # l = [token, timestamp, nonce]
    # l.sort()    
    # hashcode = hashlib.sha1(l).hexdigest()
    # print("handle/GET func: hashcode, signature: ", hashcode, signature)
    return echostr


doc_string = """
- 发送中文：AI自动回复。(具有情景上下文)
- 发送图片：进行人脸识别。
- 发送\"movie [电影名]\": 可以寻找磁力链接（我从不开车 = =）
    （例\"movie 驴得水\"可以寻找电影驴得水的磁力链接）
- 发送\"douban [电影or书籍...]\"可以查看评分及豆瓣链接
- 发送\"book [书名]\"可以获得电子书（提供txt, pdf, mobi, azw多种格式）
- 发送\"music [音乐名]\"可以获得下载外链（浏览器打开直接下载）
"""

@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    result = "<h1>Hello Weixin</h1>"
    if request.method == 'POST':
        logging.info("POST")
        logging.info(request.data)
        # recv_msg = BeautifulSoup(request.data.decode('utf-8'), "lxml")
        recv_msg = etree.XML(request.data)
        to_user = recv_msg.find('ToUserName').text
        from_user = recv_msg.find('FromUserName').text
        msg_type = recv_msg.find('MsgType').text
        logging.info("to: "+to_user)
        logging.info("from: "+from_user)
        logging.info("type: "+msg_type)

        ret_content = handle_msg(msg_type, recv_msg)

        reply = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
        </xml>
        """
        reply_str = reply % (from_user, to_user, int(time.time()), ret_content)
        response = make_response(reply_str)
        response.content_type = 'application/xml'
        return response
    return result


def handle_msg(msg_type, recv_msg):
    ret_content = str()
    if msg_type == 'event':
        subscribe = recv_msg.find('Event').text
        if subscribe == 'subscribe':
            ret_content = "欢迎关注。\n你可以输入 /help 来获取使用帮助。\n"
            ret_content += doc_string

    elif msg_type == 'text':
        content = recv_msg.find('Content').text
        ret_content = content
    return ret_content

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
