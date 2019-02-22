from flask import Flask,render_template,request
import requests
import json
import pymysql


db = pymysql.connect("localhost","root","130270","wangzhe")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS HERO")
sql = """CREATE TABLE HERO(
         NUM INT(4),
         CNAME  CHAR(20),
         TITLE CHAR(20),
         SKIN CHAR(20)
          )"""
cursor.execute(sql)
url = requests.get('http://pvp.qq.com/web201605/js/herolist.json').content
jsonFile = json.loads(url)
for m in range(len(jsonFile)):
    num = jsonFile[m]['ename']  # 编号
    cname = jsonFile[m]['cname']  # 英雄名字
    title = jsonFile[m]['title']  # 英雄title
    skinName = jsonFile[m]['skin_name'] # 切割皮肤的名字，用于计算每个英雄有多少个皮肤
    skinNumber = len(skinName)

    # SQL 插入语句
    sql = "INSERT INTO hero(NUM,CNAME,TITLE,SKIN) \
           VALUES (%d,'%s','%s','%s')"%(num,cname,title,skinName)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/record', methods=['POST'])
def success():
    if request.method == 'POST':
        text = request.form['inner']
        print(text)
        return render_template('index.html', hero_num=text)


if __name__ == '__main__':
    app.run(debug=True)
