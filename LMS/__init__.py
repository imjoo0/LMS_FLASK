import traceback

from flask import Flask, render_template, g, Response, make_response, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sshtunnel import SSHTunnelForwarder
from LMS import sql
# g: 글로벌 변수(Application Context영역), 방문자수 등 모든 사용자와 공유되어야 하는 변수
# getattr(g, 'str', '111'): 글로벌 변수 g의 'str' 어트리뷰트를 표시하고, 'str' 어트리뷰트가 없을 경우 default값으로 '111'이 출력되도록 지정함.
# Application Context: 모든 사람을 위한 영역
# Session: 한 사람의 브라우저를 위한 영역
# return getarrt(g,'str','111')

app = Flask(__name__)

# app.debug = True
# db 설정
# db 설정


@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        receive_mobileno = request.form['userid']
        # teachers = sql.ssh_db_tunneling_select_teachers()
        with SSHTunnelForwarder(
                ('15.164.36.206'),
                ssh_username="ec2-user",
                ssh_pkey="D:/purple_academy_privkey.pem",
                remote_bind_address=('purple-lms-mariadb-1.cdpnol1tlujr.ap-northeast-2.rds.amazonaws.com', 3306)
        ) as tunnel:
            db = pymysql.connect(
                host='127.0.0.1', user="readonly",
                password="purpledbreadonly12!@", port=tunnel.local_bind_port, database='purple-lms'
            )
            try:
                with db.cursor() as cur:
                    print(receive_mobileno)
                    cur.execute(f'SELECT * FROM staff WHERE mobileno={receive_mobileno};')
                    print('he')
                    rows = cur.fetchall()

                    for row in rows:
                        print(row)
                    return render_template('perform.html')
            except:
                print(traceback.format_exc())
                print("fail")
                return render_template('login.html')
            finally:
                db.close()
    else:
        return render_template('login.html')

@app.route('/perform',methods=['GET'])
def perform():
    if request.method == 'GET':
        classes = sql.ssh_db_tunneling_select_class()
        print(classes)
        return render_template('perform.html',classes)

@app.route('/user')
def get_user_manage():
    return render_template('user.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)