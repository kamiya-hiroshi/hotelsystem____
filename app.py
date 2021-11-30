import os

from flask import Flask, render_template
from flask import jsonify
from flask import request
from werkzeug.utils import secure_filename

from common import mysql_operate

app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

app.config['JSON_AS_ASCII']=False
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/img/')

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/query')
def get_all_hotels():
    sql = "select * from t_hotel"
    data = mysql_operate.db.select_db(sql)
    print("获取所有的酒店信息==>> {}".format(data))
    return jsonify(data)

@app.route('/setroom', methods=["GET", "POST"])
def set_roominfo():
    roomtype = str(request.form.get('roomtype'))
    roomnum = str(request.form.get('roomnum'))
    price = str(request.form.get('price'))
    hotelroomid = str(request.form.get('hotelroomid'))
    print(format(roomtype) + "   "+format(roomnum)+"      "+format(price)+"       "+format(hotelroomid))
    sql = "insert into t_room(roomtype, roomnum, price, hotelroomid) values('"+roomtype+"','"+roomnum+"','"+price+"','"+hotelroomid+"')"
    mysql_operate.db.execute_db(sql)
    return '设置客房信息成功！'


@app.route('/sethotel', methods=["GET", "POST"])
def set_newhotel():
    hotelname = str(request.form.get('hotelname'))
    hoteladdress = str(request.form.get('hoteladdress'))
    introduction = str(request.form.get('introduction'))
    fundation = str(request.form.get('fundation'))
    star = str(request.form.get('star'))
    photourl=" "
    print(format(hotelname)+format(hoteladdress))
    # photo = request.files.get('photo')
    # photourl = str(photo.filename)
    # if photourl!=None:
    #     upload_path = os.path.join(app.config['UP_DIR'], photourl)
    #     photo.save(upload_path)
    # else:
    #     photourl=""
    # photourl = str(request.args.get('photourl'))

    sql = "insert into t_hotel(hotelname, hoteladdress, introduction, fundation, star, photourl) values('"+hotelname+"','"+hoteladdress+"','"+introduction+"','"+fundation+"', '"+star+"','"+photourl+"')"
    mysql_operate.db.execute_db(sql)

    return '设置新酒店成功！'

@app.route('/look')
def look_hotel():
    hotelid = str(request.args.get('hotelid'))
    sql = "select * from t_hotel where(hotelid = '"+hotelid+"')"
    data=mysql_operate.db.select_db(sql)
    return jsonify(data)


@app.route('/setmanager', methods=["GET", "POST"])
def set_newmanager():
    mname = str(request.form.get('mname'))
    mpwd = str(request.form.get('mpwd'))

    sql = "insert into t_manager(mname, mpwd) values('" + mname + "','" + mpwd + "')"
    mysql_operate.db.execute_db(sql)

    return '设置酒店管理人员成功！'

@app.route('/login')
def login():
    username = str(request.args.get('username'))
    password = str(request.args.get('password'))

    sql1 = "select mpwd from t_manager where (mname='"+username+"')"
    pwd1 = mysql_operate.db.select_db(sql1)
    sql2 = "select adminpwd from t_admin where (adminname='"+username+"')"
    pwd2 = mysql_operate.db.select_db(sql2)

    print("pwd1: "+format(pwd1))
    print("pwd2: "+format(pwd2))
    print(type(pwd1))
    print(format(len(pwd1))+"      "+format(len(pwd2)))
    if len(pwd2)==0 and len(pwd1)!=0:
        return "Success-Manager"
    elif len(pwd1)==0 and len(pwd2)!=0:
        return "Success-Admin"
    else:
        return "Error"

@app.route('/tohotellist')
def jump():
    return render_template("hotellist.html")

@app.route('/toupdatehotel')
def jump_update_hotel():
    return render_template("updatehotel.html")

@app.route('/set_manager')
def jump_set_manager():
    return render_template("set_manager.html")

@app.route('/set_hotel')
def jump_set_hotel():
    return render_template("set_hotel.html")

@app.route('/set_room')
def jump_set_room():
    return render_template("set_room.html")


if __name__ == '__main__':
    app.run()
