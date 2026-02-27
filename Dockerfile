FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
SHELL ["/bin/bash", "-lc"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    locales \
    git wget \
    python3 python3-pip python3-venv python3-dev \
    libreadline8 libncurses6 libtinfo6 libglib2.0-0 libpcre3 \
    build-essential autoconf automake autotools-dev bison flex pkg-config \
    libc6-dev libncurses-dev libpcre3-dev libglib2.0-dev libreadline-dev \
    default-libmysqlclient-dev \
    ca-certificates curl less && \
    locale-gen en_US.UTF-8 && update-locale LANG=C.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

COPY MMG/docker/korp-docker/cwb-3.5.0-src /tmp/cwb-3.5.0-src/
COPY MMG/docker/korp-docker/cwb-code-r1901-perl-trunk-CWB /tmp/cwb-perl

WORKDIR /tmp/cwb-3.5.0-src
RUN export CFLAGS="-O2 -Wall -fPIC" CXXFLAGS="$CFLAGS" && \
    make clean && make depend && make all && make install && \
    rm -rf /tmp/cwb-3.5.0-src

ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /tmp/cwb-perl
RUN perl Makefile.PL && make && make install && \
    rm -rf /tmp/cwb-perl

WORKDIR /opt/gorpur-aftan
COPY gorpur-aftan/requirements.txt /opt/gorpur-aftan/requirements.txt

RUN python3 -m venv /opt/gorpur-aftan-venv && \
    source /opt/gorpur-aftan-venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt --break-system-packages && \
    apt-get purge -y \
    build-essential autoconf automake autotools-dev bison flex pkg-config \
    libc6-dev libncurses-dev libpcre3-dev libglib2.0-dev libreadline-dev \
    python3-dev && \
    rm -rf /var/lib/apt/lists/* /root/.cache /tmp/*

COPY gorpur-aftan/ /opt/gorpur-aftan

RUN groupadd --system gorpur && \
    useradd --system --gid gorpur --home /opt/gorpur-aftan --shell /usr/sbin/nologin gorpur && \
    chown -R gorpur:gorpur /opt/gorpur-aftan /opt/gorpur-aftan-venv

USER gorpur

EXPOSE 1234

CMD ["bash", "-lc", "source /opt/gorpur-aftan-venv/bin/activate && python /opt/gorpur-aftan/run.py"]
