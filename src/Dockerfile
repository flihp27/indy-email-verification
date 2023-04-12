FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "/bin/sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080 --noreload" ]

# ./manage.py migrate && ./manage.py runserver 0.0.0.0:$${PORT}
# docker build -t my-python-app .
# docker run -it --rm --name my-running-app my-python-app