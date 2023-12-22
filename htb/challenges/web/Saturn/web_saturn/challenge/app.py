from flask import Flask, request, render_template
import requests
from safeurl import safeurl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            su = safeurl.SafeURL()
            opt = safeurl.Options()
            opt.enableFollowLocation().setFollowLocationLimit(0)
            su.setOptions(opt)
            su.execute(url)
        except:
            return render_template('index.html', error=f"Malicious input detected.")
        r = requests.get(url)
        return render_template('index.html', result=r.text)
    return render_template('index.html')


@app.route('/secret')
def secret():
    if request.remote_addr == '127.0.0.1':
        flag = ""
        with open('./flag.txt') as f:
            flag = f.readline()
        return render_template('secret.html', SECRET=flag)
    else:
        return render_template('forbidden.html'), 403


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1337, threaded=True)
