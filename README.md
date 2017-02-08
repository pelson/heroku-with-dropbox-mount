# About

A proof-of-concept to use FUSE to mount Dropbox on Heroku.

** Note: ultimately, this was a proof-of-concept that failed. The pre-requisites required for FUSE mount are not available to Heroku containers, though this proof-of-concept can be run locally.**

Heroku + FUSE thread on twitter: https://twitter.com/pypelson/status/828979866770870272

# Running locally

## Build

    docker build --tag testing ./

## Run

    docker run \
        --device /dev/fuse \
        --cap-add SYS_ADMIN \
        -p 5000:5000 \
        -e PORT=5000 \
        -e DROPBOX_TOKEN=<dropbox_token> \
        -t -i \
        testing


If using docker-machine, get the IP of the container with ``docker-machine ip <machine-name>``.
A web service will be running at http://<ip>:5000.

