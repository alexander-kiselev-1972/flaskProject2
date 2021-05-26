from app import db
from ..models import User, Owner, Foto, Messages, Anonymous, Campers_nav, Config
from app.models import Headers
from .forms import LeaveMessage
from app.email import send_email, send_email_user
from flask import render_template, session, redirect, url_for
import os
import time






def get_header():
    h4 = Headers.query.filter_by(id=1).first().h4_text

    return h4



def leave_messages(form):

    try:
        user = Anonymous.query.filter_by(email=form.email.data).first()
        if user is not None:
            #Вставляем в User данные из формы
            messages = Messages(subject=form.subject.data, mess=form.message.data, user_id=user.id)
            db.session.add(messages)
            db.session.commit()
            #письмо нам
            send_email(os.environ.get('FLASKY_ADMIN'), 'Сообщение от посетителя сайта',
                       'auth/email/message', user=form.first_name.data, user_subject=form.subject.data,
                       user_message=form.message.data, email=form.email.data)


            #письмо посетителю сайта
            email = str(form.email.data)
            send_email(email, 'Website visitor message',
                       'auth/email/message_for_user', user=form.first_name.data, user_subject=form.subject.data,
                       user_message=form.message.data)
            form.first_name.data = ''
            form.last_name.data = ''
            form.subject.data = ''
            form.email.data = ''
            form.message = ''
        user_new = Anonymous(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        db.session.add(user_new)
        db.session.commit()

        user_id = Anonymous.query.filter_by(email=form.email.data).first().id
        messages = Messages(subject=form.subject.data, mess=form.message.data, user_id=user_id)
        db.session.add(messages)
        db.session.commit()

        #письмо нам
        send_email(os.environ.get('FLASKY_ADMIN'), 'Сообщение от посетителя сайта',
                   'auth/email/message', user=form.first_name.data, user_subject=form.subject.data,
                       user_message=form.message.data, email=form.email.data)

        # письмо посетителю сайта
        email = str(form.email.data)
        send_email( email, 'Website visitor message',
                   'auth/email/message_for_user', user=form.first_name.data, user_subject=form.subject.data,
                   user_message=form.message.data)

        form.first_name.data = ''
        form.last_name.data = ''
        form.subject.data = ''
        form.email.data = ''
        form.message = ''
    except :
        pass


