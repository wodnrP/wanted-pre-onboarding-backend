# base image
FROM python:3.9.6

# set working directory
WORKDIR /app

COPY requirements.txt /app/
COPY . /app/
# expose port
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt && \
    rm -rf /tmp

# set environment variables
ENV PATH /py/bin:$PATH

RUN python manage.py collectstatic --noinput
CMD ["python", "manage.py", "runserver", "0:8000"]
