from flask import jsonify, g, request
from app.views import pcosView
from app.views.auth import basic_auth
from app.views.auth import token_auth
from app.models.models_user import User
from app import db


@pcosView.route('/user/login', methods=['POST'])
@basic_auth.login_required
def get_token():
    print('-------------data' )
    print(data )
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'code': 201, 'msg': "不存在该用户"})

    check_pw = user.check_password(data['password'])
    if not check_pw:
        return jsonify({'code': 201, 'msg': "密码错误"})

    token = user.get_jwt()
    # 每次用户登录（即成功获取 JWT 后），更新 last_seen 时间
    user.ping()
    db.session.commit()
    return jsonify({'code': 200, 'msg': "验证成功", 'token': token})
    ##return jsonify({'token': token})


@pcosView.route('/user/info', methods=['GET'])
@token_auth.login_required
def get_useinfo():
    user  = g.current_user
    data = {
        'username': user.username,
        'roles': [user.role.name],
        'avatar':  user.channel.logo,
        'channel': user.channel.name,
        'id': user.id
    }
    return jsonify({'code': 200, 'msg': "登录成功", 'data': data})


@pcosView.route('/user/logout', methods=['POST'])
def logout():
    return jsonify({'code': 200, 'msg': "登出成功"})
