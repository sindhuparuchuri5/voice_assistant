#!/bin/bash

# Start PulseAudio in the background with TCP support
pulseaudio --start --exit-idle-time=-1 --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/24" &

# Run the assistant
python assistant.py
