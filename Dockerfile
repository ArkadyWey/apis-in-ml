FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./src/apis_in_ml /code/apis_in_ml
 
CMD ["uvicorn", "apis_in_ml.main:app", "--host", "0.0.0.0", "--port", "80"]