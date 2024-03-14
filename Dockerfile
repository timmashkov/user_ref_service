FROM python:3.10

WORKDIR /user_ref_service


COPY requirements.txt /user_ref_service/
RUN pip install --upgrade pip; pip install  -r /user_ref_service/requirements.txt

COPY . .