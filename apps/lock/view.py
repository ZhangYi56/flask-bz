
from sqlalchemy import Column, INTEGER, MetaData, Numeric, SmallInteger, String, Table
from sqlalchemy import create_engine, inspect,tuple_,desc
from sqlalchemy.sql import text, select ,and_  ,or_, desc
from werkzeug.utils import bind_arguments
from apps.lock.models import Lock_result, MechLockRecord
from flask.blueprints import Blueprint
from flask import Flask,render_template, request, flash, redirect ,url_for, send_file
from exts import db
import io
import pandas as pd
from  urllib.parse import quote


lock_bp =Blueprint('lock',__name__)


# 主页
@lock_bp.route('/',endpoint='index',methods=['GET', 'POST'])
def lockresult():
    rs = db.session.query(Lock_result).filter(Lock_result.lockwei >= 50 ).order_by(desc(Lock_result.lockdate), desc(Lock_result.lockwei))
    return render_template('lock/lockresult.html',rs =rs)

# # 封锁原因更新
@lock_bp.route('/update', endpoint='update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        
        lockcause = request.form.get('lockcause')
        measures = request.form.get('measures')
        id = request.form.get('id')
        #
        rs = db.session.query(Lock_result).filter(Lock_result.id == id ).update({"lockcause":lockcause})
        rs2 = db.session.query(Lock_result).filter(Lock_result.id == id ).update({"measures":measures})
        # 提交
        db.session.commit()
        return redirect(url_for('lock.index'))

    else:
        id = request.args.get('id')
        lr1 = db.session.query(Lock_result).get(id)

        rs = db.session.query(MechLockRecord).filter(and_( MechLockRecord.sign == lr1.sg_sign, MechLockRecord.lockdate == lr1.lockdate, MechLockRecord.pty ==lr1.pty )
        ).order_by(MechLockRecord.matno,MechLockRecord.divno).distinct()

        return render_template('lock/update.html', lr1=lr1 ,rs =rs)

@lock_bp.route('/download_lock', endpoint='download_lock',methods=['GET','POST'])
def download_lock():
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    # df = pd.read_sql(session.query(Lock_result.lockdate, Lock_result.pty, Lock_result.sg_sign,
    # Lock_result.lockcause,Lock_result.engineer).filter(Lock_result.lockwei >= 50 ).order_by(desc(Lock_result.lockdate), desc(Lock_result.lockwei)),db.session.bind)
    rs = db.session.query(Lock_result.lockdate, Lock_result.pty, Lock_result.sg_sign,Lock_result.lockwei,Lock_result.engineer,Lock_result.lockcause,
        Lock_result.measures).filter(Lock_result.lockwei >= 50 ).order_by(desc(Lock_result.lockdate), desc(Lock_result.lockwei))
    df = pd.DataFrame(rs).round(3)
    # df.columns = rs[0].keys()
    # columns=['序号','封锁日期','产品大类','牌号','封锁重量','封锁原因','APN','PSR','钢级','工程师'
    df.to_excel(excel_writer=writer, sheet_name='Sheet1', index=False)
    writer.save()
    out.seek(0)
    #文件名中文支持
    file_name = quote('封闭明细.xlsx')
    response = send_file(out, as_attachment=True, attachment_filename=file_name)
    response.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(file_name)
    return response