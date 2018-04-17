from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)


@app.route('/weixin', methods=['GET', 'POST'])
def check():
    print(request.url)
    return 'hello'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
