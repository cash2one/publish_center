#!/bin/bash
# publish_center        Startup script for the publish_center Server

publish_center_dir=

base_dir=$(dirname $0)
publish_center_dir=${publish_center_dir:-$base_dir}
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

if [ -f ${publish_center_dir}/commands/functions ];then
    . ${publish_center_dir}/commands/functions
elif [ -f /etc/init.d/functions ];then
    . /etc/init.d/functions
else
    echo "No functions script found in [./functions, ./install/functions, /etc/init.d/functions]"
    exit 1
fi

PROC_NAME="publish_center"
lockfile=/var/lock/subsys/${PROC_NAME}

start() {
        ops_start=$"Starting ${PROC_NAME} service:"
        if [ -f $lockfile ];then
             echo -n "publish_center is running..."
             success "$ops_start"
             echo
        else
            daemon $publish_center_dir/venv/bin/python $publish_center_dir/run_publish_server.py &> /dev/null 2>&1 &
            sleep 1
            echo -n "$ops_start"
            ps axu | grep 'run_publish_server' | grep -v 'grep' &> /dev/null
            if [ $? == '0' ];then
                success "$ops_start"
                if [ ! -e $lockfile ]; then
                    lockfile_dir=`dirname $lockfile`
                    mkdir -pv $lockfile_dir
                fi
                touch "$lockfile"
                echo
            else
                failure "$ops_start"
                echo
            fi
        fi
}


stop() {
    echo -n $"Stopping ${PROC_NAME} service:"
    ps aux | grep -E 'run_publish_server.py' | grep -v grep | awk '{print $2}' | xargs kill -9 &> /dev/null
    ret=$?
    if [ $ret -eq 0 ]; then
        echo_success
        echo
        rm -f "$lockfile"
    else
        echo_failure
        echo
        rm -f "$lockfile"
    fi

}

status(){
    ps axu | grep 'run_publish_server' | grep -v 'grep' &> /dev/null
    if [ $? == '0' ];then
        echo -n "publish_center is running..."
        success
        touch "$lockfile"
        echo
    else
        echo -n "publish_center is not running."
        failure
        echo
    fi
}



restart(){
    stop
    start
}

# See how we were called.
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;

  restart)
        restart
        ;;

  status)
        status
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 2
esac
