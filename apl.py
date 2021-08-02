# from _typeshed import Self
import flask
import pymysql
from flask import jsonify,render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["get"])
def login():
    return render_template('login.html')

@app.route("/select", methods=["get","post"])
def home():
    return render_template('select.html')
    
@app.route("/daterangepicker.js", methods=["get","post"])
def JS():
    return render_template('./daterangepicker.js')

@app.route("/select/table/<select>/<select1>/<select2>/<select3>", methods=["get"])
def table(select,select1,select2,select3):
    return render_template('table.html',webselect = select,webselect1 = select1,webselect2 = select2,webselect3 = select3)

# ========================== GET DATA ====================================

def db_test():
    db = pymysql.connect(host='localhost',user='porter',passwd='pn12345',db='test')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db,cursor

@app.route("/select/<SourceIP>/<starttime>/<endtime>/<FQDN>", methods=["get"])
def gettablejson(SourceIP,starttime,endtime,FQDN) :
    db, cursor = db_test()
    ip = ''
    FQ = ''
    if SourceIP == 'all':
        ip = "%"
    else:
        ip = SourceIP

    if FQDN == 'all':
        FQ = "%"
    else:
        FQ = FQDN
    
    sql = """
            SELECT CONVERT(Date,CHAR) as Date, CONVERT(Time,CHAR) as Time, usec, SourceIP, SourcePort, DestinationIP, DestinationPort, FQDN
            FROM (SELECT CONCAT(Date,'_',Time) as datetime, Date, Time, usec, SourceIP, SourcePort, DestinationIP, DestinationPort, FQDN FROM test.test) as t1
            where SourceIP like '{}' and datetime BETWEEN '{}' AND '{}' and FQDN like '{}';
        """.format(ip,starttime,endtime,FQ)
    cursor.execute(sql)
    data = cursor.fetchall()
    db.close()
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)