FROM python:3.11.4-alpine 

WORKDIR /usr/src/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure python output is sent directly to terminal 
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY entrypoint.sh .


RUN chmod +x entrypoint.sh

ENTRYPOINT ["tail", "-f", "/dev/null"]

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]