FROM python:3.12

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "python3 app.py & python3 appespecialista.py"]
