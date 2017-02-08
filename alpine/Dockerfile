FROM alpine:latest

# Install python and pip
RUN apk add --update python py-pip bash ca-certificates

RUN apk add fuse

# Add our code
ADD ./ /opt/webapp/
WORKDIR /opt/webapp

RUN adduser -D myuser
RUN chown -R  myuser /opt/webapp
USER myuser

CMD python webapp.py

