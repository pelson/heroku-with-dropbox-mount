#Grab the latest alpine image
FROM continuumio/miniconda

# Mod-probe is an undocumented dependency on fuse
RUN apt-get update --fix-missing
RUN apt-get install fuse --yes

ADD rules.d/99-fuse.rules /etc/udev/rules.d/99-fuse.rules

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -qr /tmp/requirements.txt

# Run the image as a non-root user
RUN adduser myuser

# Add our code
COPY ./ /opt/webapp/
RUN chown -R myuser /opt/webapp
WORKDIR /opt/webapp


USER myuser
ENV PATH /opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
CMD 'ls'

#python webapp.py

