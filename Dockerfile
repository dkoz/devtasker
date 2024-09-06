FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9050

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9050", "app:app"]