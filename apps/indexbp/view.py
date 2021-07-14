
from flask.blueprints import Blueprint
from flask import render_template



index_bp = Blueprint('index_bp',__name__)


# 主页
@index_bp.route('/',endpoint='index',methods=['GET', 'POST'])
def index():
    return render_template('index_bp/index.html')

