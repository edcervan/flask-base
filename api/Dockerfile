# base image
FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install pip==24.3.1
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod -R 777 /app

EXPOSE 5000

# Run the app when the container launches
CMD ["/bin/bash", "entrypoint.sh"]

#CMD ["python3", "app.py"]
