#!/bin/bash

pulseaudio --start --exit-idle-time=-1 --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/24" &

python assistant.py
