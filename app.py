from flask import Flask, render_template, request, json, session, redirect, url_for
import pymysql

app = Flask(__name__)
conn = pymysql.connect(host='127.0.0.1', port=3307, user="root", passwd='a1234', db="demo", charset='utf8')
conn.set_charset('utf8mb4')
cur = conn.cursor()
app.secret_key = 'any random string'


@app.route('/')
def intro():
    if session:
        return redirect(url_for('main'))
    else:
        return render_template('login.html')

@app.route('/create/board/userinfo', methods=['GET', 'POST'])
def userinfo():
    empno = session['empno']
    query = "SELECT users.entry,dept.name FROM users, dept WHERE empno = %s" % empno
    cur.execute(query)
    datas = cur.fetchone()
    date = '%s-%s-%s' % (datas[0].year, datas[0].month, datas[0].day)
    return date

@app.route('/craete/userinfo/dept')
def userdept():
    empno = session['empno']
    query = "SELECT dept.name from dept,users where users.empno=%s" % empno
    cur.execute(query)
    datas = cur.fetchone()
    print(datas[0])
    return json.dumps(datas[0])


@app.route('/create/board', methods=['GET', 'POST'])
def helloworld():
    title = request.form['title']
    text = request.form['ir1']
    query = "INSERT INTO boards(title,content) VALUES(%s, %s)"
    cur.execute(query, (title, text))
    print(" create board ! ")
    conn.commit()
    return '제목 : '+ title + '<br> 내용 : ' + text + '<br><button onclick=window.parent.location.href="/">MAIN</button>'

@app.route('/boards/table')
def showform():
    return render_template('boardtable.html')

@app.route('/main')
def main():
    empno = session['empno']
    name = session['name']
    rank = session['rank']
    return render_template('main.html', empno=empno, name=name, rank=rank)

@app.route('/create')
def student():
    return render_template('createboard.html')

@app.route('/creates/<no>')
def creboard(no):
    empno = session['empno']
    query = "SELECT users.entry,dept.name FROM users, dept WHERE empno = %s and dept.deptno=users.deptno" % empno
    cur.execute(query)
    datas = cur.fetchone()
    date = '%s-%s-%s' % (datas[0].year, datas[0].month, datas[0].day)
    dept = datas[1]
    return render_template('inputboard.html', board_no=no, name=session['name'], rank= session['rank'],date = date, dept=dept )


@app.route('/showboard', methods=['GET', 'POST'])
def showboard():
    query = 'SELECT * FROM board_form'
    cur.execute(query)
    _data = cur.fetchall()
    boarddata = []
    for a, b,c in _data:
        wish_dict = [
            a,
            b
        ]
        boarddata.append(wish_dict)
    return json.dumps({'data' : boarddata}, sort_keys=False)

@app.route('/board/<id_>')
def boarddata(id_):
    query = 'SELECT * FROM boards where board_id=%s' % id_
    cur.execute(query)
    _data = cur.fetchall()
    return render_template('board.html', content=_data)


@app.route('/boardcontent', methods=['GET', 'POST'])
def boardcontent():
    no = request.form['_id']
    query = "SELECT form_code from board_form where boardno = %s " % no
    cur.execute(query)
    board_form = cur.fetchone()
    return board_form[0]


@app.route('/login', methods=['GET', 'POST'])
def login():
    _id= request.form['user_id']
    _pass= request.form['user_password']
    if _id and _pass:
        query = "SELECT users.empno,users.name,comrank.rankname FROM users, comrank where users.id='%s' and users.pass='%s' and comrank.rankno=users.rankno" % (_id, _pass)
        cur.execute(query)
        user_data = cur.fetchall()
        if user_data:
            for a,b,c in user_data:
                session['empno'] = a
                session['name'] = b
                session['rank'] = c

            return redirect(url_for('main'))
        else:
            return '<script>alert("아이디 / 패스워드를 확인해주세요"); location.href="/"</script>'
    else:
        return '<script>alert("아이디 비밀번호 모두 입력해주세요"); location.href="/"</script>'

@app.route('/TEST')
def dateTEST():
    return render_template('TEST.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('intro'))


if __name__ == "__main__":
    app.run(debug=True)
    