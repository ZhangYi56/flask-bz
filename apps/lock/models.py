from exts import db
from ibm_db_sa.base import DOUBLE


class Lock_result(db.Model):
    __tablename__ = 'lock_result'
    __table_args__ = {'schema': 'steelplate'}

    id =db.Column( db.INTEGER,primary_key=True)
    lockdate =db.Column( db.String(30))
    pty =db.Column( db.String(5))
    sg_sign =db.Column( db.String(50))
    lockwei =db.Column( db.DECIMAL)
    lockcause =db.Column( db.String(1000))
    apn =db.Column( db.String(8))
    psr =db.Column( db.String(20))
    steelcode =db.Column( db.String(20))
    engineer =db.Column( db.String(30))
    measures =db.Column(db.String(500))

    def __str__(self):
        return self.lockdate,self.pty,self.lockdate,self.sg_sign,self.lockwei,self.lockcause,self.engineer

class MechLockRecord(db.Model):
    __tablename__ = 'mech_lock_records'
    __table_args__ = {'schema': 'steelplate'}

    matno = db.Column(db.String(80), primary_key=True, nullable=False)
    divno = db.Column(db.String(10), primary_key=True, nullable=False)
    divweight = db.Column(db.DECIMAL)
    sign = db.Column(db.String(80))
    psr = db.Column(db.String(20))
    pchjudgecode = db.Column(db.String(10))
    procstatus = db.Column(db.String(10))
    remarkdiv = db.Column(db.String(200))
    steel = db.Column(db.String(20))
    orderno = db.Column(db.String(50))
    STANDARD = db.Column(db.String(80))
    productflag = db.Column(db.String(80))
    slabno = db.Column(db.String(20))
    pono = db.Column(db.String(20))
    oldpsr = db.Column(db.String(20))
    oldapn = db.Column(db.String(20))
    oldmic = db.Column(db.String(20))
    matordthick = db.Column(db.Float)
    matordwidth = db.Column(db.SmallInteger)
    matordlen = db.Column(db.SmallInteger)
    procflag = db.Column(db.String(20))
    dutyunit = db.Column(db.String(10))
    remark = db.Column(db.String(100))
    coldjudgecode1 = db.Column(db.String(100))
    coldjudgecode2 = db.Column(db.String(100))
    coldjudgecode3 = db.Column(db.String(100))
    coldjudgecode4 = db.Column(db.String(100))
    coldjudgecode5 = db.Column(db.String(100))
    coldjudgecode6 = db.Column(db.String(100))
    coldjudgecode7 = db.Column(db.String(100))
    coldjudgecode8 = db.Column(db.String(100))
    coldjudgecode9 = db.Column(db.String(100))
    coldjudgecode10 = db.Column(db.String(100))
    lockdate = db.Column(db.String(20))
    judgedate = db.Column(db.String(20))
    judgeresult = db.Column(db.String(50))
    degradewei = db.Column(db.Float)
    department = db.Column(db.String(50))
    unit = db.Column(db.String(10))
    pty = db.Column(db.String(10))
    flg = db.Column(db.String(20))
    creatortag = db.Column(db.String(80))