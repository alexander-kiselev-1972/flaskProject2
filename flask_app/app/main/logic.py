from app import db
from ..models import User, Owner, Foto, Messages,  Campers_nav, Config, ModelCamp
from app.models import Headers, Config, models_dict
from .forms import LeaveMessage
from app.email import send_email, send_email_user
from flask import render_template, session, redirect, url_for, signals, g
import os
import time
import json

def get_model_to_list(name_models):
    try:
        list_models = name_models.query.all()
    except Exception as e:
        print("Ошибка ", e)
        list_models = []
    return list_models



def prepare_data_for_index_configuration():
    data_list = []

    try:
        models = ModelCamp.query.all()
        for i in models:
            data_dict = {}
            for key, data in i.items():
                data_dict[key] = data

            data_list.append(data_dict)
    except Exception as e:
        print("Ошибка ", e)

    return data_list



def get_header():
    h4 = Headers.query.filter_by(id=1).first().h4_text

    return h4



def leave_messages(form):
    """Логика для нижней формы"""

    try:

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            #session['user_id'] = user.id
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
        user_new = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        db.session.add(user_new)
        db.session.commit()

        user = User.query.filter_by(email=form.email.data).first()
        #session['user_id'] = user.id
        user_id = user.id
        messages = Messages(subject=form.subject.data, mess=form.message.data, user_id=user_id)
        db.session.add(messages)
        db.session.commit()

        #письмо нам
        send_email(os.environ.get('FLASKY_ADMIN'), 'Сообщение от посетителя сайта',
                   'auth/email/message', user=form.first_name.data, user_subject=form.subject.data,
                       user_message=form.message.data, email=form.email.data)

        # письмо посетителю сайта
        token = user.generate_confirmation_token()
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


def get_data(model):
    model_data = model.query.all()
    return model_data



