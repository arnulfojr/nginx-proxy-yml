#!/bin/sh

set -e

echo 'Container ready...'

nginx-helper docker_preview /proxy.yml

nginx-helper from_docker /proxy.yml /etc/nginx/conf.d/default.conf

# debug mode
if [ "${1}" = 'debug' ]; then
  echo 'Debug mode activated'
  exec nginx-debug -g 'daemon off;'
fi

# serve mode
if [ "${1}" = 'serve' ]; then
  exec nginx -g 'daemon off;'
fi

# update config
if [ "${1}" = 'update' ]; then
  exec nginx -s reload
  echo 'nginx reloaded'
fi

echo "Command not registered will execute: '${@}'"
exec "${@}"
