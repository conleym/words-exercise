 #! /bin/bash

if [ "$1" = 'dispy' ]; then
    shift;
    /usr/local/bin/dispynode.py -i "0.0.0.0" --daemon "$@"
else
    exec "$@"
fi
