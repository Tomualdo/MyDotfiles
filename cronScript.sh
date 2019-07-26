#!/bin/sh

if ps -ef | grep -v grep | grep miner ; then
  echo running
  exit 0
else
  echo not running
  /home/tom/Downloads/webchain-miner-2.8.0-linux-amd64/webchain-miner
  exit 0
fi
