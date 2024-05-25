FROM python:3.12.3-alpine

COPY src/. .

RUN pip install -r requirements.txt

CMD ["python", "./api_requester.py"]
