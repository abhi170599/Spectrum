FROM python:3.7

# install cython dependencies
# RUN apt-get -y install libc-dev
# RUN apt-get -y install build-essential
# RUN pip install -U pip 
# RUN apk --no-cache add lapack libstdc++ && apk --no-cache add --virtual .builddeps g++ gcc gfortran musl-dev lapack-dev && pip install scipy && pip install gensim && apk del .builddeps && rm -rf /root/.cache

 
# copy everything to the working directory
COPY . /app 

# change the working directory
WORKDIR /app 

# upgrade pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# nltk corpus
RUN python -m nltk.downloader punkt


# EXPOSE REST API PORT
EXPOSE 5001 

ENTRYPOINT [ "python" ]

# command to start the app
CMD [ "main.py" ]