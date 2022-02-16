FROM python:3

WORKDIR /usr/local/identitysmsapi

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY sendSmsApi.py .

EXPOSE 8580

CMD ["python3","./sendSmsApi.py"]