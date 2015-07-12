#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User,Role,Post,Comment
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)
app.debug=True

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post)
    
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """run tests"""
    import unittest
    tests=unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
    
if __name__=='__main__':
    
    manager.run()
