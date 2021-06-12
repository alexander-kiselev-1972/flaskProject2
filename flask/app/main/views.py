from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from . import main
from .forms import LeaveMessage
from .. import db
from .logic import get_header, leave_messages
from ..models import User, Owner, Foto, Messages, Anonymous, Campers_nav, Config
from flask_login import login_user, current_user
from app.email import send_email
import os

@main.route('/', methods=['GET', 'POST'])
def index():
    h4 = get_header()
    own = Owner.query.all()

    campers_nav = Campers_nav.query.all()
    foto = Foto.query.all()
    config = Config.query.all()

    form = LeaveMessage()

    if form.validate_on_submit():
        leave_messages(form)
        return redirect(url_for(".index"))

    return render_template('main3/index.html', h4=h4, own=own, form=form, models=config)






@main.route('/cookie')
def cookie():
    return render_template('cookie.html')
