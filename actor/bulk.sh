#!/bin/bash

echo "Hello Friend, which folder do you want to work on today?"
read FOLDER

CWD="$(pwd)"
#echo $CWD/$FOLDER


if [ -d "${CWD}/${FOLDER}" ]; then
        echo "checking if \"$CWD/$FOLDER\" has evtx files"
        if [ `find -type f |grep "$FOLDER"|grep -E 'evtx$'|wc -l` -ne 0 ]; then 
                echo "Working..."
                for E in `find -type f |grep $FOLDER|grep evtx`; do echo $E && script.py "$E"  "$E.xml" ;done
                cd ${FOLDER}/
                echo "... done"
                echo "Doing cleanup ..."
                for E in `find -type f|  grep -E 'evtx$'`; do rm $E ;done
                for E in `find -type f`; do mv $E "`echo $E | sed s/.evtx.xml/.xml/`"  ;done
                echo "... cleanup finished."
                cd  ..
                echo "tarring up my work..."
                tar czf ${FOLDER}.tgz ${FOLDER}
                echo "${FOLDER}.tgz created"
                echo "What a pleasure to help you today."
                echo ""
        else
        echo "\"$CWD/$FOLDER\" does not contain .evtx files, cant help you today"
        fi
else 
        echo "\"$CWD/$FOLDER\" does not exists, cant help you today"
fi
