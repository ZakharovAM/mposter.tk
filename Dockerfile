FROM python:3.7-alpine

ENV FLASK_APP app.py
RUN mkdir /mposter
WORKDIR /mposter
COPY ./mposter/boot.sh boot.sh
COPY ./mposter/requirements.txt requirements.txt
COPY ./mposter/app.py app.py
COPY ./mposter/main.py main.py
COPY ./mposter/templates templates
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN chmod +x boot.sh
EXPOSE 5000
RUN source ./venv/bin/activate
ENTRYPOINT ["./boot.sh"]
