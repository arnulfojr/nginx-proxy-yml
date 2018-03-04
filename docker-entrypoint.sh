#!/bin/sh

set -e

echo 'Container ready...'

nginx-helper load /services.yml /etc/nginx/conf.d/default.conf

# debug mode
if [ "${1}" = 'debug' ]; then
  echo 'Debug mode activated'
  nginx-helper preview /services.yml
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
