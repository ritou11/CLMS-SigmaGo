FROM django:onbuild
ADD packages/wechat-0.1.0-py3.6.egg wechat.egg
RUN easy_install -i http://mirrors.aliyun.com/pypi/simple/ wechat.egg
RUN tar -zxvf packages/pycrypto-2.6.1.tar.gz
WORKDIR pycrypto-2.6.1
RUN python setup.py install
WORKDIR ../