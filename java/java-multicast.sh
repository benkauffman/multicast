#!/usr/bin/env bash

./java-udp-server/java-server.sh &
./java-udp-client/java-client.sh

pkill -f java-server.sh