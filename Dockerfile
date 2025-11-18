FROM apache/hadoop:3

USER root

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*.repo && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo && \
    sed -i 's|vault.centos.org|vault.epel.cloud|g' /etc/yum.repos.d/epel*.repo || true && \
    yum clean all -y && \
    yum makecache fast

RUN yum install -y python3 python3-pip && \
    yum clean all && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3    /usr/bin/pip

USER hadoop