FROM python:3.10-alpine

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD gunicorn app:"app" -b 0.0.0.0:5000 --reload  
# CMD python3 /app.py