#! /bin/bash

cd /opt/stack/new/scrutinize
export EVENTLET_NO_GREENDNS=yes

#stop n-api

echo "Killing Nova-api"
kill -9 `ps aux | grep -v grep | grep nova-api | awk '{print $2}'`
sleep 10
if (( $(ps -ef | grep -v grep | grep nova-api | wc -l) >= 0 ))
then
   echo "nova-api is running!!!"
else
echo "starting nova-pi"
sudo scrutinize /opt/stack/new/scrutinize/example/scrutinize-nova-api.json /usr/local/bin/nova-api >/opt/stack/new/screen-logs/screen-n-api.log 2>&1 & echo $! >/opt/stack/status/stack/n-api.pid
fi

#stop nova-scheduler

echo "Killing nova-scheduler"
kill -9 `ps aux | grep -v grep | grep nova-scheduler | awk '{print $2}'`
if (( $(ps -ef | grep -v grep | grep nova-scheduler | wc -l) > 0 ))
then
echo "nova-scheduler is running!!!"
else
echo "Starting nova-scheduler"
sudo scrutinize /opt/stack/new/scrutinize/example/scrutinize-nova-sch.json /usr/local/bin/nova-scheduler >/opt/stack/new/screen-logs/screen-n-sch.log 2>&1 --config-file /etc/nova/nova.conf & echo $! >/opt/stack/status/stack/n-sch.pid;
fi

#stop nova-compute

echo "killing nova-compute"
kill -9 `ps aux | grep -v grep | grep nova-compute | awk '{print $2}'`
if (( $(ps -ef | grep -v grep | grep nova-compute | wc -l) > 0 ))
then
echo "nova-compute is running!!!"
else
sudo scrutinize /opt/stack/new/scrutinize/example/scrutinize-nova-compute.json /usr/local/bin/nova-compute >/opt/stack/new/screen-logs/screen-n-cpu.log 2>&1 --config-file /etc/nova/nova.conf & echo $! >/opt/stack/status/stack/n-cpu.pid
fi

#stop q-svc
echo "Killing neutron-server"
kill -9 `ps aux | grep -v grep | grep neutron-server | awk '{print $2}'`
if (( $(ps -ef | grep -v grep | grep neutron-server | wc -l) > 0 ))
then
echo "neutron-server is running!!!"
else
sudo scrutinize /opt/stack/new/scrutinize/example/scrutinize-neutron-api.json /usr/local/bin/neutron-server --config-file /etc/neutron/neutron.conf >/opt/stack/new/screen-logs/screen-q-svc.log 2>&1 --config-file /etc/neutron/plugins/ml2/ml2_conf.ini & echo $! >/opt/stack/status/stack/q-svc.pid
fi
#cd /opt/stack/new/scrutinize
#export EVENTLET_NO_GREENDNS=yes

#start n-api

#scrutinize /opt/stack/new/scrutinize/example/scrutinize-nova-api.json /usr/local/bin/nova-api >/opt/stack/new/screen-logs/screen-n-api.log 2>&1 & echo $! >/opt/stack/status/stack/n-api.pid 
#echo "Waiting for nova-api to start..."
#while ! wget --no-proxy -q -O- http://127.0.0.1:8774;
#do sleep 1; done"; then
#        echo "nova-api did not start"
#        exit 1
#echo "Done."

#cd /opt/stack/new/nova && /usr/local/bin/nova-api >/opt/stack/new/screen-logs/screen-n-api.log 2>&1 & echo $! >/opt/stack/status/stack/n-api.pid || echo "n-api failled"

# start nova-scheduler

#scrutinize /opt/stack/new/scrutinize/example/scrutinize-nova-sch.json /usr/local/bin/nova-scheduler >/opt/stack/new/screen-logs/screen-n-sch.log 2>&1 --config-file /etc/nova/nova.conf & echo $! >/opt/stack/status/stack/n-sch.pid;

#cd /opt/stack/new/nova && /usr/local/bin/nova-scheduler >/opt/stack/new/screen-logs/screen-n-sch.log 2>&1 --config-file /etc/nova/nova.conf  & echo $! >/opt/stack/status/stack/n-sch.pid || echo "failed"

# start nova-compute

#scrutinize /opt/stack/new/scrutinize/example/scrutinize-nova-compute.json /usr/local/bin/nova-compute >/opt/stack/new/screen-logs/screen-n-cpu.log 2>&1 --config-file /etc/nova/nova.conf & echo $! >/opt/stack/status/stack/n-cpu.pid

#cd /opt/stack/new/nova && /usr/local/bin/nova-compute >/opt/stack/new/screen-logs/screen-n-cpu.log 2>&1 --config-file /etc/nova/nova.conf  & echo $! >/opt/stack/status/stack/n-cpu.pid || echo "failed"

#start q-svc

#scrutinize /opt/stack/new/scrutinize/example/scrutinize-neutron-api.json /usr/local/bin/neutron-server --config-file /etc/neutron/neutron.conf >/opt/stack/new/screen-logs/screen-q-svc.log 2>&1 --config-file /etc/neutron/plugins/ml2/ml2_conf.ini & echo $! >/opt/stack/status/stack/q-svc.pid
#echo "Waiting for neutron-server to start..."
#if ! timeout 60 sh -c "while ! wget --no-proxy -q -O- http://127.0.0.1:9696;
#do sleep 1; done"; then
#        echo "neutron-server did not start"
#        exit 1
#fi
#echo "Done."
#cd /opt/stack/new/neutron && python /usr/local/bin/neutron-server --config-file /etc/neutron/neutron.conf >/opt/stack/new/screen-logs/screen-q-svc.log 2>&1 --config-file /etc/neutron/plugins/ml2/ml2_conf.ini & echo $! >/opt/stack/status/stack/q-svc.pid || echo "failed"

#echo "all services started"
