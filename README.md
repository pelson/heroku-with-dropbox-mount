

Running locally
---------------

    docker build --tag testing ./
    docker run -p 5000:5000 -e PORT=5000 testing

If using docker-machine, get the IP of the container with ``docker-machine ip <machine-name>``.

