# Stage 1: Fuente oficial de binarios de Apache Hadoop 3.3.6
FROM apache/hadoop:3.3.6 AS hadoop-binaries

# Stage 2: Sistema operativo base Ubuntu 22.04 LTS
FROM ubuntu:22.04

LABEL maintainer="Tecsup - Inteligencia de Negocios"
LABEL description="Entorno Hadoop 3.3.6 distribuido/pseudo-distribuido sobre Ubuntu Linux con soporte Python y Java"

ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalar dependencias esenciales, Java 11, Python 3 y utilitarios Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    openssh-server \
    openssh-client \
    rsync \
    sudo \
    curl \
    python3 \
    python3-pip \
    nano \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# 2. Configurar usuario ubuntu con privilegios sudo sin contraseña
RUN useradd -m -s /bin/bash -u 1000 ubuntu && \
    echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 3. Configurar SSH sin contraseña para localhost (requerido por daemons de Hadoop)
USER ubuntu
WORKDIR /home/ubuntu

RUN ssh-keygen -t rsa -P '' -f /home/ubuntu/.ssh/id_rsa && \
    cat /home/ubuntu/.ssh/id_rsa.pub >> /home/ubuntu/.ssh/authorized_keys && \
    chmod 0600 /home/ubuntu/.ssh/authorized_keys

# 4. Copiar Hadoop 3.3.6 desde la etapa oficial y ajustar permisos
USER root
COPY --from=hadoop-binaries --chown=ubuntu:ubuntu /opt/hadoop /opt/hadoop

# Crear directorios para NameNode, DataNode y temporales con permisos de usuario ubuntu
RUN mkdir -p /opt/hadoop/data/nameNode /opt/hadoop/data/dataNode /opt/hadoop/data/tmp /opt/hadoop/logs && \
    chown -R ubuntu:ubuntu /opt/hadoop/data /opt/hadoop/logs && \
    chmod -R 777 /opt/hadoop/data /opt/hadoop/logs

# 5. Configurar variables de entorno globales en /etc/environment y ~/.bashrc
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_INSTALL=$HADOOP_HOME
ENV HADOOP_MAPRED_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_HOME=$HADOOP_HOME
ENV HADOOP_HDFS_HOME=$HADOOP_HOME
ENV YARN_HOME=$HADOOP_HOME
ENV HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin:$JAVA_HOME/bin

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_HOME=/opt/hadoop" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_INSTALL=\$HADOOP_HOME" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_MAPRED_HOME=\$HADOOP_HOME" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_COMMON_HOME=\$HADOOP_HOME" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_HDFS_HOME=\$HADOOP_HOME" >> /home/ubuntu/.bashrc && \
    echo "export YARN_HOME=\$HADOOP_HOME" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_COMMON_LIB_NATIVE_DIR=\$HADOOP_HOME/lib/native" >> /home/ubuntu/.bashrc && \
    echo "export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop" >> /home/ubuntu/.bashrc && \
    echo "export PATH=\$PATH:\$HADOOP_HOME/sbin:\$HADOOP_HOME/bin:\$JAVA_HOME/bin" >> /home/ubuntu/.bashrc && \
    echo "export PS1='\[\e[01;32m\]ubuntu@laptop\[\e[00m\]:\[\e[01;34m\]\w\[\e[00m\]\$ '" >> /home/ubuntu/.bashrc

# 6. Script de arranque del contenedor
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER ubuntu
WORKDIR /home/ubuntu

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
