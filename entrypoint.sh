#!/bin/bash
set -e

# Iniciar servicio SSH para comunicación interna entre daemons
sudo service ssh start

# Configuración para evitar prompt de verificación de clave en localhost
if [ ! -f /home/ubuntu/.ssh/config ]; then
    echo -e "Host *\n   StrictHostKeyChecking no\n   UserKnownHostsFile=/dev/null" > /home/ubuntu/.ssh/config
    chmod 600 /home/ubuntu/.ssh/config
fi

exec "$@"
