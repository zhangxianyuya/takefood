from flask import Flask, jsonify, request
from sqlalchemy import text

from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
import auth
import datetime
from redis import StrictRedis



# 创建redis对象,Redis是一个高性能的内存数据库，常用于缓存和消息队列。启动Redis服务使你的应用程序能够连接和使用Redis。
redis_store = StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)

# 添加配置数据库
app.config.from_object(BaseConfig)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())

#安装用户口令哈希存储所需要的库
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#用户注册
@app.route("/api/user/register", methods=["POST"])
@cross_origin()
def user_register():
    rq = request.json
    username = rq.get("username")
    password = rq.get("password")
    telephone = rq.get("telephone")
    role = rq.get("role")
    real_name = rq.get("real_name")
    age = rq.get("age")
    sex = rq.get("sex")
    mail = rq.get("mail")

    # 将密码进行哈希处理
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # 检查手机号是否已经存在
    data = db.session.execute(text('select * from user where telephone=:telephone'), {"telephone": telephone}).fetchall()
    if not data:
        # 插入 user 表
        db.session.execute(text(
            'insert into user(username, password, telephone, role) values(:username, :password, :telephone, :role)'),
            {"username": username, "password": hashed_password, "telephone": telephone, "role": role})
        db.session.commit()

        # 获取新插入用户的 ID
        new_user_id = db.session.execute(text('select id from user where telephone=:telephone'), {"telephone": telephone}).fetchone()[0]

        # 插入 user_msg 表
        db.session.execute(text(
            'insert into user_msg(id, real_name, sex, age, mail, phone, user_name) values(:id, :real_name, :sex, :age, :mail, :phone, :user_name)'),
            {"id": new_user_id, "real_name": real_name, "sex": sex, "age": age, "mail": mail, "phone": telephone, "user_name": username})
        db.session.commit()

        return jsonify({"status": 200, "msg": "注册成功"})
    else:
        return jsonify({"status": 1000, "msg": "该用户已存在"})

#用户登录
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():
    #print(request.json) 调试语句
    userortel = request.json.get("userortel").strip()
    password = request.json.get("password").strip()
    role = request.json.get("role")

    # 根据手机号和角色信息查询数据库
    sql = 'select * from user where telephone = :telephone and role = :role'
    data = db.session.execute(text(sql), {"telephone": userortel, "role": role}).first()
    if data:
        hashed_password = data[2]
        if bcrypt.check_password_hash(hashed_password, password):
            user = {'id': data[0], 'username': data[1], 'telephone': data[3]}
            token = auth.encode_func(user)
            return jsonify({"code": 200, "msg": "登录成功", "token": token, "role": data[4]})
        else:
            return jsonify({"code": 1000, "msg": "用户名或密码错误"})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})


#忘记密码
@app.route("/api/user/findback", methods=["POST"])
@cross_origin()
def forgot_password():
    print(request.json)  # 调试语句，检查接收到的 JSON 数据
    rq = request.json
    telephone = rq.get("telephone")
    password = rq.get("password")

    # 检查新密码是否为空
    if not password:
        return jsonify({"status": 1001, "msg": "新密码不能为空"})

    # 检查手机号是否存在
    data = db.session.execute(text('select * from user where telephone=:telephone'), {"telephone": telephone}).first()
    if data:
        # 将新密码进行哈希处理
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # 更新用户的密码
        db.session.execute(text('update user set password=:password where telephone=:telephone'), {"password": hashed_password, "telephone": telephone})
        db.session.commit()

        return jsonify({"status": 200, "msg": "密码重置成功"})
    else:
        return jsonify({"status": 1000, "msg": "该手机号未注册"})



# 用户界面获取店铺信息
@app.route("/api/user/shop", methods=["GET"])
@cross_origin()
def user_get_shop():
    try:
        data = db.session.execute(text('select * from fastfood_shop')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(shop_name=data[i][0], price=data[i][1], sale=data[i][2], hp_num=data[i][3], cp_num=data[i][4],shop_tel = data[i][5])
            Data.append(dic)
        print("Retrieved shop data:", Data)  # 打印获取到的店铺数据
        return jsonify(status=200, tabledata=Data)
    except Exception as e:
        print("Error retrieving shop data:", e)  # 打印获取数据时出现的错误
        return jsonify(status=500, msg="Error retrieving shop data")


#店铺好评差评数量
@app.route("/api/shop/review/count", methods=["GET"])
@cross_origin()
def get_review_count():
    if request.method == 'GET':
        shop_name = request.args.get('shop_name')
        try:
            # 查询对应店铺的好评数和差评数
            review_counts = db.session.execute(text('SELECT hp_num, cp_num FROM fastfood_shop WHERE shop_name=:shop_name'), {"shop_name": shop_name}).fetchone()
            if review_counts:
                hp_num = review_counts['hp_num']
                cp_num = review_counts['cp_num']
                return jsonify(status=200, hp_num=hp_num, cp_num=cp_num)
            else:
                return jsonify(status=400, msg="找不到对应店铺的评价信息")
        except Exception as e:
            return jsonify(status=500, msg="获取评价数量失败，错误信息：{}".format(e))

# 下订单
@app.route("/api/user/addorder", methods=["POST"])
@cross_origin()
def user_addorder():
    rq = request.json
    shopname = rq.get("shop_name")
    ordermoney = rq.get("order_money")
    orderway = rq.get("order_way")
    consphone = get_token_phone(request.headers.get('token'))
    consname = rq.get("cons_name")
    consaddre = rq.get("cons_addre")
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    from sqlalchemy.sql import text
    # 使用参数化查询
    query = text(
        'insert into oorder(shop_name, order_money, order_way, cons_phone, cons_name, cons_addre, create_time) values(:shop_name, :order_money, :order_way, :cons_phone, :cons_name, :cons_addre, :create_time)')
    db.session.execute(query, {
        'shop_name': shopname,
        'order_money': ordermoney,
        'order_way': orderway,
        'cons_phone': consphone,
        'cons_name': consname,
        'cons_addre': consaddre,
        'create_time': create_time
    })
    db.session.commit()

    return jsonify(status=200, msg="成功下单")


def get_token_phone(token):
    data = auth.decode_func(token)
    phone = data['telephone']
    return phone

#用户未发货订单
@app.route("/api/user/unsend", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_unsend():
    from sqlalchemy import text
    if request.method == 'GET':
        phone = get_token_phone(request.headers.get('token'))
        print(phone)
        from sqlalchemy.sql import text

        # 使用参数化查询，防止sql注入
        query = text('select * from oorder where checked=0 and cons_phone=:phone')
        data = db.session.execute(query, {'phone': phone}).fetchall()

        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2], orderway=data[i][3],
                       cons_name=data[i][5], cons_addre=data[i][6], create_time=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get("order_id")
        cons_name = rq.get("cons_name")
        cons_addre = rq.get("cons_addre")
        print(order_id)
        db.session.execute(
            text('update oorder set cons_name="%s", cons_addre="%s" where order_id="%d"' % (cons_name, cons_addre, order_id)))
        db.session.commit()
        return jsonify(status=200, msg="修改成功")
    if request.method == 'DELETE':
        order_id = request.json.get("delete_id")
        db.session.execute(text('delete from oorder where order_id="%d" ' % order_id))
        db.session.commit()
        return jsonify(status=200, msg="删除成功")


# 用户已发货订单
@app.route("/api/user/sending", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_sending():
    # 处理GET请求
    if request.method == 'GET':
        # 从请求头中获取token，并通过get_token_phone函数获取对应的用户手机号
        phone = get_token_phone(request.headers.get('token'))

        # 执行数据库查询，获取用户的已发货订单
        data = db.session.execute(text('select * from sending_order where cons_phone="%s"' % phone)).fetchall()

        # 初始化一个空列表，用于存储订单数据
        Data = []

        # 遍历查询结果，将每一行数据转换为字典并添加到Data列表中
        for i in range(len(data)):
            dic = dict(
                order_id=data[i][0],
                shop_name=data[i][1],
                order_money=data[i][2],
                order_way=data[i][3],
                cons_phone=data[i][4],
                cons_name=data[i][5],
                cons_addre=data[i][6],
                disp_id=data[i][7],
                deliver_time=data[i][8],
                disp_phone=data[i][9]
            )
            Data.append(dic)

        # 返回JSON响应，包含状态码和订单数据
        return jsonify(status=200, tabledata=Data)


# 用户已完成订单
@app.route("/api/user/sended", methods=["POST", "GET", "DELETE"])
@cross_origin()
def user_sended():
    # 处理GET请求
    if request.method == 'GET':
        # 从请求头中获取token，并通过get_token_phone函数获取对应的用户手机号
        phone = get_token_phone(request.headers.get('token'))

        # 执行数据库查询，获取用户的已完成订单
        data = db.session.execute(text('select * from sended_order where cons_phone="%s"' % phone)).fetchall()

        # 初始化一个空列表，用于存储订单数据
        Data = []

        # 遍历查询结果，将每一行数据转换为字典并添加到Data列表中
        for i in range(len(data)):
            dic = dict(
                order_id=data[i][0],
                shop_name=data[i][1],
                order_money=data[i][2],
                order_way=data[i][3],
                cons_phone=data[i][4],
                cons_name=data[i][5],
                cons_addre=data[i][6],
                disp_id=data[i][7],
                deliver_time=data[i][8],
                disp_phone=data[i][9]
            )
            Data.append(dic)

        # 返回JSON响应，包含状态码和订单数据
        return jsonify(status=200, tabledata=Data)

#用户点击确认收货
@app.route("/api/user/confirm_receipt", methods=["POST"])
@cross_origin()
def confirm_receipt():
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get('order_id')
        try:
            # 修改数据库中对应订单的 check 字段为 2
            db.session.execute(text('update oorder set checked=2 where order_id=:order_id'), {"order_id": order_id})
            db.session.commit()

            # 更新物流表中对应订单的 ended 字段为 1
            db.session.execute(text('update wuliu set ended=1 where order_id=:order_id'), {"order_id": order_id})
            db.session.commit()

            return jsonify(status=200, msg="确认收货成功")
        except Exception as e:
            db.session.rollback()
            return jsonify(status=500, msg="确认收货失败，错误信息：{}".format(e))


#好评
@app.route("/api/shop/rate/good", methods=["POST"])
@cross_origin()
def rate_good():
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get('order_id')
        try:
            print("Received POST request to rate good with order ID:", order_id)
            app.logger.info("Received POST request to rate good with order ID: %s", order_id)
            # 检查订单是否已经评价过
            order = db.session.execute(text('SELECT rated FROM oorder WHERE order_id=:order_id'), {"order_id": order_id}).fetchone()
            print("Order details:", order)
            app.logger.info("Order details: %s", order)
            if order and order[0] == 0:  # 使用正确的整数索引访问元组中的元素
                # 更新订单状态为好评
                db.session.execute(text('UPDATE oorder SET rated=1 WHERE order_id=:order_id'), {"order_id": order_id})
                db.session.commit()
                return jsonify(status=200, msg="好评成功")
            else:
                return jsonify(status=400, msg="该订单已评价过")
        except Exception as e:
            db.session.rollback()
            error_msg = "好评失败，错误信息：{}".format(e)
            print(error_msg)
            app.logger.error(error_msg)
            return jsonify(status=500, msg=error_msg)

#差评
@app.route("/api/shop/rate/bad", methods=["POST"])
@cross_origin()
def rate_bad():
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get('order_id')
        try:
            print("Received POST request to rate bad with order ID:", order_id)
            app.logger.info("Received POST request to rate bad with order ID: %s", order_id)
            # 检查订单是否已经评价过
            order = db.session.execute(text('SELECT rated FROM oorder WHERE order_id=:order_id'), {"order_id": order_id}).fetchone()
            print("Order details:", order)
            app.logger.info("Order details: %s", order)
            if order and order[0] == 0:  # 使用正确的整数索引访问元组中的元素
                # 更新订单状态为差评
                db.session.execute(text('UPDATE oorder SET rated=2 WHERE order_id=:order_id'), {"order_id": order_id})
                db.session.commit()
                return jsonify(status=200, msg="差评成功")
            else:
                return jsonify(status=400, msg="该订单已评价过")
        except Exception as e:
            db.session.rollback()
            error_msg = "差评失败，错误信息：{}".format(e)
            print(error_msg)
            app.logger.error(error_msg)
            return jsonify(status=500, msg=error_msg)


# 用户信息
@app.route("/api/user/usermsg", methods=["POST", "GET"])
@cross_origin()
def usermsg():
    # 处理GET请求，获取用户信息
    if request.method == 'GET':
        # 从请求头中获取token，并通过get_token_phone函数获取对应的用户手机号
        phone = get_token_phone(request.headers.get('token'))

        # 执行数据库查询，获取用户信息
        data = db.session.execute(text('select * from user_msg where phone=:phone'), {"phone": phone}).fetchone()

        # 如果查询到用户信息，将其转换为字典并返回
        if data:
            Data = {
                'id': data[0], 'real_name': data[1], 'sex': data[2], 'age': data[3],
                'mail': data[4], 'phone': data[5], 'user_name': data[6]
            }
            return jsonify(status=200, data=Data)
        else:
            # 如果未查询到用户信息，返回状态码1000和错误信息
            return jsonify(status=1000, msg="用户信息未找到")
    # 处理POST请求，更新用户信息
    elif request.method == 'POST':
        # 获取请求中的JSON数据
        rq = request.json

        # 提取JSON数据中的各个字段
        id = rq.get("id")
        real_name = rq.get("real_name")
        sex = rq.get("sex")
        age = rq.get("age")
        mail = rq.get("mail")
        phone = rq.get("phone")
        user_name = rq.get("user_name")

        # 执行数据库更新操作，更新用户信息
        db.session.execute(text(
            'update user_msg set real_name=:real_name, sex=:sex, age=:age, mail=:mail, phone=:phone, user_name=:user_name where id=:id'),
            {"real_name": real_name, "sex": sex, "age": age, "mail": mail, "phone": phone, "user_name": user_name,
             "id": id})

        # 提交事务
        db.session.commit()

        # 返回状态码200和成功信息
        return jsonify(status=200, msg="修改成功")



# 修改密码
@app.route("/api/user/pwd_chg", methods=["POST"])
@cross_origin()
def user_pwd_chg():
    if request.method == 'POST':
        phone = get_token_phone(request.headers.get('token'))
        old_pwd = request.json.get('old_pwd')
        new_pwd = request.json.get('new_pwd')

        # 获取用户信息
        data = db.session.execute(text('select * from user where telephone=:telephone'), {"telephone": phone}).first()
        if data and bcrypt.check_password_hash(data[2], old_pwd):
            new_hashed_pwd = bcrypt.generate_password_hash(new_pwd).decode('utf-8')
            db.session.execute(text('update user set password=:new_password where telephone=:telephone'),
                               {"new_password": new_hashed_pwd, "telephone": phone})
            db.session.commit()
            return jsonify(status=200, msg="修改成功")
        else:
            return jsonify(status=1000, msg="原始密码错误")


# 管理员管理店铺的接口
@app.route("/api/manager/shop", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_shop():
    # 处理GET请求，获取所有店铺信息
    if request.method == 'GET':
        # 执行查询语句，获取店铺信息
        data = db.session.execute(text('SELECT * FROM fastfood_shop')).fetchall()
        Data = []
        # 遍历查询结果，构建店铺信息字典
        for row in data:
            dic = {
                'shop_name': row[0],
                'price': row[1],
                'sale': row[2],
                'hp_num': row[3],
                'cp_num': row[4],
                'shop_tel': row[5]
            }
            Data.append(dic)
        # 返回店铺信息的JSON响应
        return jsonify(status=200, tabledata=Data)

    # 从请求体中获取JSON数据
    rq = request.json

    # 处理POST请求，添加新店铺
    if request.method == 'POST' and rq.get('action') == "add":
        shop_name = rq.get('shop_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        shop_tel = rq.get('shop_tel')
        # 检查店铺是否已存在
        exist = db.session.execute(
            text('SELECT * FROM fastfood_shop WHERE shop_name=:shop_name'),
            {'shop_name': shop_name}
        ).fetchall()
        if not exist:
            # 插入新店铺信息
            db.session.execute(
                text(
                    'INSERT INTO fastfood_shop (shop_name, price, m_sale_v, shop_tel) VALUES (:shop_name, :price, :m_sale_v, :shop_tel)'),
                {'shop_name': shop_name, 'price': int(price), 'm_sale_v': int(m_sale_v), 'shop_tel': shop_tel}
            )
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该店铺已存在")

    # 处理POST请求，修改店铺信息
    if request.method == 'POST' and rq.get('action') == "change":
        shop_name = rq.get('shop_name')
        price = rq.get('price')
        m_sale_v = rq.get('m_sale_v')
        shop_tel = rq.get('shop_tel')
        # 更新店铺信息
        db.session.execute(
            text(
                'UPDATE fastfood_shop SET price=:price, m_sale_v=:m_sale_v, shop_tel=:shop_tel WHERE shop_name=:shop_name'),
            {'price': int(price), 'm_sale_v': int(m_sale_v), 'shop_tel': shop_tel, 'shop_name': shop_name}
        )
        db.session.commit()
        return jsonify(status=200, msg="修改成功")

    # 处理DELETE请求，删除店铺信息
    if request.method == 'DELETE':
        want_delete = rq.get('want_delete')
        # 删除指定店铺信息
        db.session.execute(
            text('DELETE FROM fastfood_shop WHERE shop_name=:shop_name'),
            {'shop_name': want_delete}
        )
        db.session.commit()
        return jsonify(status=200, msg="删除成功")

#管理员管理服务员
@app.route("/api/manager/server", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_server():
    if request.method == 'GET':
        # 执行查询语句，获取所有服务员信息
        data = db.session.execute(text('select * from server')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(service_id=data[i][0], service_name=data[i][1], fastfood_shop_name=data[i][2])
            Data.append(dic)
        # 执行查询语句，获取所有店铺名称
        shop_range = db.session.execute(text('select shop_name from fastfood_shop')).fetchall()
        Shop = []
        for i in range(len(shop_range)):
            dic = dict(shop_name=shop_range[i][0])
            Shop.append(dic)
        # 打印店铺名称范围（便于调试）
        print(Shop)
        return jsonify(status=200, tabledata=Data, shop_range=Shop)
    # 处理POST请求，添加新服务员
    if request.method == 'POST':
        rq = request.json
        service_id = rq.get('service_id')
        service_name = rq.get('service_name')
        fastfood_shop_name = rq.get('fastfood_shop_name')
        # 检查服务员是否已存在
        exist = db.session.execute(text('select * from server where service_id="%s"' % service_id)).fetchall()
        if not exist:
            # 插入新服务员信息
            db.session.execute(text('insert server(service_id,service_name,fastfood_shop_name) value("%s","%s","%s")' % (
                service_id, service_name, fastfood_shop_name)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该编号已存在")
    # 处理DELETE请求，删除服务员信息
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        # 删除指定服务员信息
        db.session.execute(text('delete from server where service_id="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="解雇成功")


#管理员管理送餐员
@app.route("/api/manager/dispatcher", methods=["POST", "GET", "DELETE"])
@cross_origin()
def manager_dispatcher():
    # 处理GET请求，获取所有送餐员信息
    if request.method == 'GET':
        data = db.session.execute(text('select * from dispatcher')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(dispatcher_id=data[i][0], dispatcher_name=data[i][1], dispatcher_phone=data[i][2])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    # 处理POST请求，添加新送餐员
    if request.method == 'POST':
        rq = request.json
        dispatcher_id = rq.get('dispatcher_id')
        dispatcher_name = rq.get('dispatcher_name')
        dispatcher_phone = rq.get('dispatcher_phone')
        # 检查送餐员是否已存在
        exist = db.session.execute(text('select * from dispatcher where dispatcher_id="%s"' % dispatcher_id)).fetchall()
        if not exist:
            # 插入新送餐员信息
            db.session.execute(
                text('insert dispatcher(dispatcher_id,dispatcher_name,dispatcher_phone) value("%s","%s","%s")' % (
                    dispatcher_id, dispatcher_name, dispatcher_phone)))
            db.session.commit()
            return jsonify(status=200, msg="添加成功")
        else:
            return jsonify(status=1000, msg="该编号已存在")
    # 处理DELETE请求，删除送餐员信息
    if request.method == 'DELETE':
        want_delete = request.json.get('want_delete')
        # 删除指定送餐员信息
        db.session.execute(text('delete from dispatcher where dispatcher_id="%s"' % want_delete))
        db.session.commit()
        return jsonify(status=200, msg="解雇成功")


#管理员界面物流
@app.route("/api/manager/wuliu", methods=["GET"])
@cross_origin()
def manager_wuliu():
    # 获取请求参数中的 'id' 值，用于判断物流状态
    ended = request.args.get('id')
    if ended == '0':
        # 查询未结束的物流信息（ended=0）
        data = db.session.execute(text('select * from wuliu where ended=0')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)
    else:
        # 查询已结束的物流信息（ended=1）
        data = db.session.execute(text('select * from wuliu where ended=1')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], cons_phone=data[i][1], disp_id=data[i][2], deliver_time=data[i][3])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


#管理员界面未发货订单
@app.route("/api/manager/unsend", methods=["GET", "POST"])
@cross_origin()
def manager_unsend():
    if request.method == 'GET':
        # 查询所有未发货的订单（checked=0）
        data = db.session.execute(text('select * from oorder where checked=0')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], price=data[i][2], orderway=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], create_time=data[i][8])
            Data.append(dic)

        # 获取所有送货员的ID，供选择
        disp_range = db.session.execute(text('select * from dispatcher')).fetchall()  # 获取所有的送货员就id，供选择
        Disp_range = []
        for i in range(len(disp_range)):
            dic = dict(disp_id=disp_range[i][0])
            Disp_range.append(dic)
        return jsonify(status=200, tabledata=Data, disp_range=Disp_range)
    if request.method == 'POST':
        rq = request.json
        order_id = rq.get('order_id')
        disp_id = rq.get('dispatcher_id')
        deliver_time = rq.get('deliver_time')
        # 获取指定订单的收货人电话
        cons_phone = db.session.execute(text('select cons_phone from oorder where order_id="%d"' % int(order_id))).first()

        # 插入物流信息
        db.session.execute(text('insert wuliu( order_id, cons_phone,disp_id,deliver_time) value(%d,"%s","%s","%s")' % (
        int(order_id), cons_phone[0], disp_id, deliver_time)))
        db.session.commit()
        return jsonify(status=200, msg="成功派发")


#管理员界面已发货订单
@app.route("/api/manager/sending", methods=["GET"])
@cross_origin()
def manager_sending():
    if request.method == 'GET':
        # 查询所有已发货的订单
        data = db.session.execute(text('select * from sending_order')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


#管理员界面已完成订单
@app.route("/api/manager/sended", methods=["GET"])
@cross_origin()
def manager_sended():
    if request.method == 'GET':
        # 查询所有已完成的订单
        data = db.session.execute(text('select * from sended_order')).fetchall()
        Data = []
        for i in range(len(data)):
            dic = dict(order_id=data[i][0], shop_name=data[i][1], order_money=data[i][2], order_way=data[i][3],
                       cons_phone=data[i][4],
                       cons_name=data[i][5], cons_addre=data[i][6], disp_id=data[i][7], deliver_time=data[i][8])
            Data.append(dic)
        return jsonify(status=200, tabledata=Data)


if __name__ == '__main__':
    app.run(debug=True)
