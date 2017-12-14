FROM django:onbuild
RUN tar -zxvf packages/pycrypto-2.6.1.tar.gz
WORKDIR pycrypto-2.6.1
RUN python setup.py install
WORKDIR ../