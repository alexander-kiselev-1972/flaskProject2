FROM python:3.8

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

ENV SECRET_KEY='lkhgcykjuigtycv6543545gv__cffyuoidsert'
ENV DEV_DATABASE_URL='postgresql+psycopg2://postgres:oSaka_2019@localhost:5434/campers4'
ENV FLASK_APP=flasky.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=True

RUN pip install -r requirements.txt

CMD ["flask", "run"]
