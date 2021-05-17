from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Owner

@main.route('/', methods=['GET', 'POST'])
def index():
    own = Owner.query.all()
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for(".index"))

    return render_template('main/index.html', own=own, form=form)


@main.route('/cookie')
def cookie():
    return render_template('cookie.html')
