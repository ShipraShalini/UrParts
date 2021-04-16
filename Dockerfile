FROM python:3.8-slim
RUN apt update && apt install postgresql-client -y && apt autoremove
WORKDIR /app
RUN pip3 install -qU pip wheel setuptools
COPY requirements.txt /app
RUN pip3 install -qr requirements.txt
COPY ./ /app
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "UrParts.wsgi"]
