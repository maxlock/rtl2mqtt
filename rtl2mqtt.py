#!/usr/bin/python

# pip2 install python-daemon lockfile

import daemon
import daemon.pidfile
import paho.mqtt.client as paho
import simplejson as json
from subprocess import Popen, PIPE, STDOUT

def do_something():
  mqttc = paho.Client()
  mqttc.connect('homeassistant.technoghetto.int')
  mqttc.loop_start()
  process = Popen(['/usr/local/bin/rtl_433','-qG','-F','json'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
  for line in iter(process.stdout.readline, ''):
    msg={}
    try:
      msg=json.loads(line)
      mqtopic='rtl_433/'+msg.get('brand','unknown').lower().replace(" ", "_")+'/'+msg.get('model','unknown').lower().replace(" ", "_")+'/'+str(msg.get('id','unknown')).lower().replace(" ", "_")
      mqpayload=json.dumps(msg)
      mqttc.publish(mqtopic,mqpayload,qos=0,retain=False)
    except ValueError:
      pass

def run():
  with daemon.DaemonContext(
    working_directory='/tmp',
    umask=0o002,
    pidfile=daemon.pidfile.PIDLockFile('/var/run/rtl2mqtt.pid'),
    ) as context:
    do_something()

if __name__ == "__main__":
  run()
