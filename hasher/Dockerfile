FROM tensorflow/tensorflow:2.15.0-gpu

WORKDIR /app

COPY weights /root/.deepface/weights

RUN apt-get update && apt-get install -y gcc libgl1-mesa-glx
RUN apt-get install -y libgl1 libglib2.0-0

COPY requirements.txt requirements.txt

RUN pip uninstall -y enum34 && pip install --ignore-installed --upgrade-strategy only-if-needed -r requirements.txt

COPY main.py /app/

CMD [ "/app/main.py" ]
