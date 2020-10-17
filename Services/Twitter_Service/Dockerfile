FROM python:alpine3.7

# copy everything to the working directory
COPY . /app 

# change the working directory
WORKDIR /app 

# install dependencies
RUN pip install -r requirements.txt

# EXPOSE REST API PORT
EXPOSE 5002 

ENTRYPOINT [ "python" ]

# command to start the app
CMD [ "main.py" ]