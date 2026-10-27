export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
export HADOOP_OS_TYPE=${HADOOP_OS_TYPE:-$(uname -s)}

# Supresión de advertencias nativas de log4j para evitar que los scripts de shell traten los warnings como nombres de host
export HADOOP_OPTS="-Dlog4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR $HADOOP_OPTS"
export HADOOP_HOME_WARN_SUPPRESS=1
export HDFS_NAMENODE_USER=ubuntu
export HDFS_DATANODE_USER=ubuntu
export HDFS_SECONDARYNAMENODE_USER=ubuntu
export YARN_RESOURCEMANAGER_USER=ubuntu
export YARN_NODEMANAGER_USER=ubuntu
