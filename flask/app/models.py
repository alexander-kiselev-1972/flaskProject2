from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic', passive_deletes=True)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Bayer': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return  self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    mess = db.relationship('Messages', backref='message', passive_deletes=True)



    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False



    def is_administrator(self):
        return False

#login_manager.anonymous_user = Anonymous()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Owner(db.Model):
    __tablename__='own'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, default='Deilmann s.r.o.')
    email1 = db.Column(db.String(128), default='karavan@deilmann.sk')
    email2 = db.Column(db.String(128))
    email3 = db.Column(db.String(128))
    phone1 = db.Column(db.String(30), unique=True, default='+421-950-764-554')
    phone2 = db.Column(db.String(30), unique=True)
    phone3 = db.Column(db.String(30), unique=True)
    icho = db.Column(db.String, unique=True)
    ulica_dom = db.Column(db.String(128))
    index = db.Column(db.String(24))
    text = db.Column(db.Text)

    def getOwn(self):
        own = Owner.query.all()


    def setOwn(self, name, email1, email2='', email3=''):
        own = Owner(name=name, email1=email1, email2=email2,email3=email3)
        db.session.add(own)
        db.session.commit()


    def __repr__(self):
        return self.name, self.email1, self.phone1, self.ulica_dom, self.index, self.icho



class Foto(db.Model):
    __tablename__='foto'
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    images = db.Column(db.String(256))

    def __repr__(self):
        return self.name, self.images


class Messages(db.Model):
    __tablename__='messages'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128))
    mess = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return self.subject, self.mess





class ModelCamp(db.Model):
    __tablename__ = 'model_camp'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    model = db.relationship("Config", backref='model', passive_deletes=True)
    #manufacturer = db.Column(db.Integer, db.ForeignKey('manufactured.id', ondelete='CASCADE'))
   # manufactured = db.relationship('Manufactured', backref='manufactur', passive_deletes=True)
    #config = db.relationship('Config', backref='model',  passive_deletes=True)

    def __init__(self, **kwargs):
        super(ModelCamp, self).__init__(**kwargs)
        if self.name is None:
            self.name = "Veles"
            self.manufacturer = 1

    # @staticmethod
    # def set():
    #     c = Model_camp(name="Veles", manufacturer=1)
    #     db.session.add(c)
    #     db.session.commit()




    def __repr__(self):
        return self.name





class Manufactured(db.Model):
    __tablename__='manufactured'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    telegramm = db.Column(db.String(64))
    model = db.Column(db.Integer, db.ForeignKey('model_camp.id', ondelete='CASCADE'))
    #camper = db.relationship('Model_camp', backref='Manufactura', lazy='dynamic', passive_deletes=True)

    def __init__(self, **kwargs):
        super(Manufactured, self).__init__(**kwargs)
        if self.name is None:
            self.name = "Enisey"
            self.email = "enisey@kolesey.ru"
            self.telegramm = "54637"

    @staticmethod
    def set():
        manufact = Manufactured(name="Enisey", email="enisey@kolesey.ru", telegramm="54637")
        db.session.add(manufact)
        db.session.commit()

    def __repr__(self):
        return self.name, self.telegramm

class Config(db.Model):
    __tablename__='config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    mattress_id = db.Column(db.Integer, db.ForeignKey('mattress.id', ondelete='CASCADE'))

    model_id = db.Column(db.Integer, db.ForeignKey("model_camp.id", ondelete='CASCADE'))


    def __repr__(self):
        return self.name


class Mattress(db.Model):
    __tablename__='mattress'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    config = db.relationship('Config', backref='mattress',  passive_deletes=True)




    def __repr__(self):
        return self.name


class Campers_nav(db.Model):
    __tablename__='campers_nav'
    id = db.Column(db.Integer, primary_key=True)
    h2_teg = db.Column(db.String(32), default="Karavan")
    p_teg = db.Column(db.Text, default="malý mobilný dom, ideálny na pohodlnú rekreáciu v prírode. Vhodný pre rybárov, poľovníkov a na\
                        cestovanie. Vyrobený v konfigurácii prívesu „teardrop“, kde miesto na spanie a kuchynský modul\
                        sú umiestnené v samostatných priehradkách. Izolované sú steny, strop a podlaha. Najväčšia\
                        prípustná celková hmotnosť prívesu nepresahuje 750 kg.")

    def __repr__(self):
        return self.h2_teg, self.p_teg



class Headers(db.Model):
    __tablename__="header"
    id = db.Column(db.Integer, primary_key=True)
    h4_text = db.Column(db.String(256), default='Ponúkame vám kompaktné multifunkčné mini karavany!')

    def __repr__(self):
        return self.h4_text


models_dict = {
    "User":User,
    "Role":Role,
    "Owner":Owner,
    "Foto":Foto,
    "Messages": Messages,
    "ModelCamp":ModelCamp,
    "Anonimous":Anonymous,
    "Manufactured":Manufactured,
    "Config":Config,
    "Campers_nav":Campers_nav,
    "Mattress":Mattress,
    "Headers":Headers
}