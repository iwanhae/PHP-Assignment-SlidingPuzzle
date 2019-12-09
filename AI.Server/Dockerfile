FROM tensorflow/tensorflow:2.0.0-py3
WORKDIR /root
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]