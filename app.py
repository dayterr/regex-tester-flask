import re
import sys

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# write your code here

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regex = db.Column(db.String(50))
    text = db.Column(db.String(1024))
    result = db.Column(db.Boolean)

db.create_all()

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        regex = request.form.get('regex')
        text = request.form.get('text')
        result = True if re.search(regex, text) else False
        record = Record(regex=regex, text=text, result=result)
        db.session.add(record)
        db.session.commit()
        return redirect(f'/result/{record.id}')
        return render_template('main.html', is_result=True, is_true=result)
    return render_template('main.html')


@app.route('/result/<int:res_id>/')
def result(res_id):
    result = Record.query.get(res_id)
    return render_template('result.html', result=result)


@app.route('/history/')
def history():
    results = Record.query.all()
    return render_template('history.html', results=results)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
