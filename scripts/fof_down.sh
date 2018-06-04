#!/bin/bash
while getopts :u:n:p:w:d:s: option
do
    case $option
    in
        u) user=$OPTARG;;
        n) hostname=$OPTARG;;
        p) port=$OPTARG;;
        w) password=$OPTARG;;
        d) db=$OPTARG;;
        s) skip=$OPTARG;;
    esac
done

dir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

if [ -v password ]
then
    python "$dir/../fof/python/down.py" -u $user -ho $hostname -p $port -d $db -pa $password
else 
    python "$dir/../fof/python/down.py" -u $user -ho $hostname -p $port -d $db
fi
