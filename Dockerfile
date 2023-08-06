# base image
FROM python:3.9.6

# set working directory
WORKDIR /app

COPY requirements.txt /app/
COPY . /app/

ENV PATH /py/bin:$PATH

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    rm -rf /tmp

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# expose port
EXPOSE 8000

# set environment variables
# ENV PYTHONUNBUFFERD 1
# RUN python manage.py collectstatic --noinput
# CMD python manage.py runserver 0.0.0.0:8000
