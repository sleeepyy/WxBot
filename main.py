from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import hashlib

app = Flask(__name__)


# /weixin?signature=b50cb9c0bbf196b3cb3bc8f42b89eeee65a090d0&echostr=457557273493372605&timestamp=1523967673&nonce=1003935488
@app.route('/weixin', methods=['GET', 'POST'])
def verify():
    print(request.url)
    signature = request.args.get('signature')
    echostr = request.args.get('echostr')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    token = 'shuxuewuli'
    
    l = [token, timestamp, nonce]
    l.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, l)
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return echostr
    else:
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
