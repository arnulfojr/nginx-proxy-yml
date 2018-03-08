#!/bin/sh

set -e

echo 'Container ready...'
echo "command: ${@}"

# serve
if [ "${1}" = 'debug' -o "${1}" = 'serve' ]; then

  if [ "${2}" = 'docker' ]; then
    nginx-helper preview docker /proxy.yml
    nginx-helper load docker /proxy.yml /etc/nginx/conf.d/default.conf
  else
    nginx-helper preview file /proxy.yml
    nginx-helper load file /proxy.yml /etc/nginx/conf.d/default.conf
  fi

  echo 'Nginx is running in debug mode'
  exec nginx-debug -g 'daemon off;'
fi

# update config
if [ "${1}" = 'update' ]; then
  exec nginx -s reload
  echo 'nginx reloaded'
fi

echo "Command not registered will execute: '${@}'"
exec "${@}"
