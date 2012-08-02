#!/bin/sh

pegasus_repository="/var/lib/Pegasus/repository"

function usage()
{
    printf "Usage: $0 [ register | unregister ] mof reg\n"
}

function register()
{
    mof=$1
    reg=$2
    if [ $HAS_SFCBD -eq 1 ];
    then
        /usr/bin/sfcbstage -r $reg $mof
        /usr/bin/sfcbrepos -f
        /usr/bin/systemctl reload-or-try-restart sblim-sfcb.service
    fi

    if [ $HAS_PEGASUS -eq  1 ];
    then
        /usr/sbin/cimserver --status > /dev/null 2>&1
        if [ $? -eq 0 ];
        then
            CIMMOF="/usr/bin/cimmof"
        else
            CIMMOF="/usr/bin/commofl -R $pegasus_repository"
        fi

        $CIMMOF -uc $mof
        cat $reg | /usr/bin/python2 $(dirname $0)/reg2pegasus.py | $CIMMOF -uc -n root/PG_Interop -
    fi
}

function unregister()
{
    mof=$1
    reg=$2
    if [ $HAS_SFCBD -eq 1 ];
    then
        /usr/bin/sfcbunstage -r $(basename $reg) $(basename $mof)
        /usr/bin/sfcbrepos -f
        /usr/bin/systemctl reload-or-try-restart sblim-sfcb.service
    fi

    if [ $HAS_PEGASUS -eq 1 ];
    then
        for provider in $(sed -n 's/ *location: *//p' $reg | sort | uniq);
        do
            /usr/bin/cimprovider -d -m ${provider} && /usr/bin/cimprovider -r -m ${provider}
        done
    fi
}

if [ $# -lt 3 ];
then
    usage
    exit 1
fi

if [ -e /usr/sbin/sfcbd ];
then
    HAS_SFCBD=1
else
    HAS_SFCBD=0
fi

if [ -e /usr/sbin/cimserver ];
then
    HAS_PEGASUS=1
else
    HAS_PEGASUS=0
fi

# TODO: check if at least one server is installed

case $1 in
    register)
        register $2 $3
        break;;
    unregister)
        unregister $2 $3
        break;;
    **)
        usage
        exit 1
esac
