from flask import Flask,render_template, request, flash,Blueprint
from pandas.core.frame import DataFrame
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from sqlalchemy import Column, INTEGER, MetaData, Numeric, SmallInteger, String, Table
from sqlalchemy import create_engine, inspect,tuple_
from sqlalchemy.sql import text, select ,and_  ,or_
import pandas as pd

mt_bp =Blueprint('mt',__name__)
""" 根据输入的卷号，导出该卷号涉及的材料履历DataFrame
    采用Like，可以模糊查询，比如%和_  """
def mat_track(coil):
    
    # 设置数据库
    eng = create_engine('ibm_db_sa://048113:048113@190.2.242.173:60000/saspub')
    
    with eng.connect() as con:

        metadata = MetaData()

        t_tmm0005 = Table(
            'tmm0005', metadata,
            Column('rec_creator', String(24)),
            Column('rec_create_time', String(14)),
            Column('rec_revisor', String(24)),
            Column('rec_revise_time', String(14)),
            Column('archive_flag', String(1)),
            Column('archive_stamp_no', String(10)),
            Column('tc_seq_no', String(20)),
            Column('mat_track_no', String(20), index=True),
            Column('out_mat_no', String(20), index=True),
            Column('mat_kind', String(4)),
            Column('mat_seq_no', INTEGER, index=True),
            Column('pre_unit_code', String(4), index=True),
            Column('whole_backlog_seq', SmallInteger),
            Column('whole_backlog_code', String(2)),
            Column('st_no', String(20)),
            Column('sg_sign', String(50)),
            Column('mat_act_thick', Numeric(6, 3)),
            Column('mat_act_width', Numeric(5, 1)),
            Column('mat_act_len', Numeric(12, 3)),
            Column('mat_act_wt', Numeric(15, 6)),
            Column('mat_act_inner_dia', SmallInteger),
            Column('mat_act_outer_dia', SmallInteger),
            Column('wt_method_code', String(1)),
            Column('prod_end_time', String(14), index=True),
            Column('order_no', String(10)),
            Column('plan_no', String(10)),
            Column('repair_flag', String(1)),
            Column('hold_flag', String(1)),
            Column('hold_cause_code', String(4)),
            Column('hold_maker', String(24)),
            Column('div_flag', String(1)),
            Column('mat_union_flag', String(1)),
            Column('mat_return_flag', String(1)),
            Column('in_mat_no_1', String(20), index=True),
            Column('in_mat_no_2', String(20)),
            Column('in_mat_no_3', String(20)),
            Column('in_mat_kind', String(4)),
            schema='mm00'
        )
        
        # 仅查询输入卷的单条mm0005信息，导出结果为ResultS rs1，最多查询前30个
        stm1 =select([t_tmm0005.c.mat_track_no]).where(t_tmm0005.c.out_mat_no.like(coil)).distinct().limit(31)
        rs1 = con.execute(stm1)

        #输入卷的单条mm0005信息变为DataFrame df1
        df1 = pd.DataFrame(rs1,columns=['mat_track_no']) 
        

        #输入模糊卷的mm0005信息导出涉及卷的所有材料跟踪号array清单  mat_track_nos 
        mat_track_nos =df1['mat_track_no'].unique()
        #新增空表df2
        df2 = pd.DataFrame(columns=['出口卷号','材料跟踪号','生产机组','生产时间','入口卷号','材料顺序号'
            ,'出钢记号','合同号','厚度','宽度','长度','牌号','重量','封锁标记','封锁原因','回退标记'])
        #循环遍历mat_track_nos清单
        for mt in mat_track_nos:
            #查询遍历的材料跟踪号 mt 涉及的所有前后工序的mm0005信息，导出结果未ResultS rs2
            stm2 =select([t_tmm0005.c.out_mat_no, t_tmm0005.c.mat_track_no, t_tmm0005.c.pre_unit_code, t_tmm0005.c.prod_end_time, t_tmm0005.c.in_mat_no_1,
            t_tmm0005.c.mat_seq_no, t_tmm0005.c.st_no, t_tmm0005.c.order_no, t_tmm0005.c.mat_act_thick, t_tmm0005.c.mat_act_width, t_tmm0005.c.mat_act_len
            ,t_tmm0005.c.sg_sign, t_tmm0005.c.mat_act_wt,t_tmm0005.c.hold_flag,t_tmm0005.c.hold_cause_code,t_tmm0005.c.mat_return_flag]).where(t_tmm0005.c.mat_track_no.like(mt)).distinct().order_by(t_tmm0005.c.mat_track_no,t_tmm0005.c.mat_seq_no)

            rs2 = con.execute(stm2)
            #该材料跟踪号涉及的所有前后工序的mm0005信息，导出结果为tempdf
            tempdf = pd.DataFrame(rs2,columns=['出口卷号','材料跟踪号','生产机组','生产时间','入口卷号','材料顺序号'
            ,'出钢记号','合同号','厚度','宽度','长度','牌号','重量','封锁标记','封锁原因','回退标记'])

            #tempdf 清单加入df2，首次加入时df2为空，后续不断上下拼接
            df2 = pd.concat([df2,tempdf],axis=0)
        #最终return  该材料跟踪号涉及的所有前后工序的mm0005信息  的DataFrame
        return df2

# 卷号表单类，新建表单wtforms，验证仅使用DataRequired空验证
class CoilForm(FlaskForm):
    #coil 为表单的输入值
    coil = StringField('卷号', validators=[DataRequired()])
    #submit 为表单的提交键
    submit = SubmitField('提交')

# 网页逻辑
@mt_bp.route('/',methods=['GET', 'POST'])

def index():
    # new一个新表单coil_Form
    coil_Form = CoilForm()

    #如果表单请求方式为request
    if request.method == 'POST':
        #进行表单验证，通过的话
        if coil_Form.validate_on_submit():
            #coil 为表单的输入值 赋值给coil_name
            coil_name = coil_Form.coil.data

            #使用def mat_track(coil)  函数，求出DataFrame df值
            df = mat_track(coil_name)
            #返回给模板 materialTracking.html，表单coil_Form，表单输入值求出的DataFrame df 转化为html tables
            return render_template('material_tracking/materialTracking.html', coil_Form = coil_Form 
                ,tables=[df.to_html(classes='data', header="true")])
        else:
        # 6. 表单验证不通过就提示错误
            flash('卷号错误')
    else:
        return render_template('material_tracking/materialTracking.html', coil_Form = coil_Form)


