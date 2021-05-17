# этот файл должен стартовать он должен быть прописан в
# FLASK_APP = flasky.py


import os
from app import create_app, db
from app.models import Permission,User, Role, models_dict
from flask import redirect, url_for, request
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
import flask_login



app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)



class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login"))


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if current_user.is_authenticated:
            print(current_user.id, "djn")
            user = User.query.filter_by(id=current_user.id).first()
            if user.role_id == 3:
                return True
            return False
        return False


    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth.login"))

admin = Admin(app, index_view=MyAdminIndexView())

for i in models_dict:
    admin.add_view(MyModelView(models_dict[i], db.session))



@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
