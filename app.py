from apps import create_app
from apps.lock.models import Lock_result
import pandas as pd

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db

# flask设置app

# app.secret_key = 'secretzy'

# Base = declarative_base()

app = create_app()
manager =Manager(app=app)

migrate = Migrate(app=app,db=db)
manager.add_command('db',MigrateCommand)

# 主程序
if __name__ == '__main__':    
    app.run(host='0.0.0.0',port = 5555, threaded=True)






