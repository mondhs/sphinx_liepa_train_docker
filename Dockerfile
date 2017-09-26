FROM ubuntu:16.04

Maintainer mondhs bus<mondhs@gmail.com>
##### Extend docker mashine to 50G
# docker machine -D create -d virtualbox --virtualbox-disk-size "50000" default
##### Build docker
#docker build -t sphinx_liepa_train .
##### Bash interface
#docker run  -v $(realpath ./LIEPA_garsynas)/LIEPA_garsynas:/data -it mondhs/sphinx_liepa_train bash
#### Web wrapper
#docker run -p 8081:8081 -p 8082:8082 -v $(realpath ./LIEPA_garsynas):/data -it mondhs/sphinx_liepa_train




COPY opt /opt


###################### INSTALL Kaldi ##############################


RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade  && \
  apt-get install -y --no-install-recommends apt-utils git ca-certificates curl sudo\
        build-essential gawk zlib1g-dev automake autoconf wget libtool subversion python libatlas3-base \
        bison python-dev swig

# SphinxBase
RUN git clone https://github.com/cmusphinx/sphinxbase.git /opt/sphinxbase --depth 1
WORKDIR "/opt/sphinxbase"
RUN ./autogen.sh
RUN  ./configure
RUN make
RUN make install


RUN git clone https://github.com/cmusphinx/pocketsphinx.git /opt/pocketsphinx --depth 1
WORKDIR "/opt/pocketsphinx"
RUN ./autogen.sh
RUN  ./configure
RUN make
RUN make install



RUN git clone https://github.com/cmusphinx/sphinxtrain.git /opt/sphinxtrain --depth 1
WORKDIR "/opt/sphinxtrain"
RUN ./autogen.sh
RUN  ./configure
RUN make
RUN make install



RUN mkdir -p /opt/sphinx_liepa_train/liepa_audio
RUN ln -s /data/train_repo /opt/sphinx_liepa_train/liepa_audio/train
RUN ln -s /data/test_repo /opt/sphinx_liepa_train/liepa_audio/test
RUN ln -s /data/sphinx_files/feat /opt/sphinx_liepa_train/feat
RUN ln -s /data/sphinx_files/etc /opt/sphinx_liepa_train/etc




############################### Web Wrapper ##########################################

#Web training wrapper
RUN git clone  https://github.com/mondhs/nodejs_kaldi_train_wrapper.git /opt/wrapper --depth 1
RUN rm -rf /opt/wrapper/contol_files
RUN ln -s /opt/sphinx_liepa_train /opt/wrapper/contol_files

RUN curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
RUN sudo apt-get install -y nodejs
WORKDIR "/opt/wrapper"
RUN npm install ws --save
CMD ["npm", "start"]

############################### CLEAN UP ##########################################

RUN rm -rf /opt/sphinxtrain
RUN rm -rf /opt/pocketsphinx
RUN rm -rf /opt/sphinxbase
RUN rm -rf /var/lib/apt/lists/*
