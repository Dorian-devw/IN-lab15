#!/bin/bash
# ==============================================================================
# PIPELINE COMPLETO DE HADOOP HDFS + YARN + MAPREDUCE (SEMMA - BIG DATA BI)
# ==============================================================================
set -e

echo "======================================================================"
echo " 1. FORMATEANDO SISTEMA DE ARCHIVOS DISTRIBUIDO HDFS (NameNode)"
echo "======================================================================"
if [ ! -d "/opt/hadoop/data/nameNode/current" ]; then
    hdfs namenode -format -force -nonInteractive
    echo "[OK] NameNode formateado correctamente."
else
    echo "[INFO] NameNode ya se encuentra formateado."
fi

echo ""
echo "======================================================================"
echo " 2. INICIANDO SERVICIOS DISTRIBUIDOS DE HADOOP (HDFS y YARN)"
echo "======================================================================"
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

echo ""
echo "======================================================================"
echo " 3. VERIFICANDO DAEMONS ACTIVOS CON JPS"
echo "======================================================================"
jps

echo ""
echo "======================================================================"
echo " 4. REPORTE DE SALUD DEL CLUSTER HDFS"
echo "======================================================================"
hdfs dfsadmin -report

echo ""
echo "======================================================================"
echo " 5. CARGA DEL DATASET DE ENERGIA A HDFS (INGESTA BIG DATA)"
echo "======================================================================"
hdfs dfs -mkdir -p /smart_grid/input
hdfs dfs -rm -r -f /smart_grid/output || true
hdfs dfs -put -f /home/ubuntu/dataset/smart_grid_energy_data.csv /smart_grid/input/
hdfs dfs -ls -h /smart_grid/input

echo ""
echo "======================================================================"
echo " 6. EJECUTANDO PROCESAMIENTO MAPREDUCE (HADOOP STREAMING)"
echo "======================================================================"
STREAMING_JAR=$(ls /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -n 1)

hadoop jar "$STREAMING_JAR" \
    -files /home/ubuntu/mapreduce/mapper.py,/home/ubuntu/mapreduce/reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input /smart_grid/input/smart_grid_energy_data.csv \
    -output /smart_grid/output

echo ""
echo "======================================================================"
echo " 7. RESULTADOS DEL ANALISIS DE EFICIENCIA ENERGETICA Y EMISIONES CO2"
echo "======================================================================"
hdfs dfs -cat /smart_grid/output/part-*

echo ""
echo "======================================================================"
echo " [COMPLETADO] El pipeline de Inteligencia de Negocios se ejecutó con éxito."
echo "======================================================================"
