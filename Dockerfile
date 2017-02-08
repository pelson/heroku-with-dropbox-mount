FROM ubuntu:latest

# Install python and pip
RUN apt-get update
RUN apt-get install --yes python python-pip ca-certificates

RUN apt-get install --yes fuse
RUN pip install tornado dropbox futures

# Add our code
ADD ./ /opt/webapp/
WORKDIR /opt/webapp

RUN useradd -m myuser && \
    chown -R  myuser /opt/webapp
USER myuser

CMD python webapp.py

