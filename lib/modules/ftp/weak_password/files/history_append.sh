#!/bin/bash

shopt -s histappend
PROMPT_COMMAND="history -a;$PROMPT_COMMAND"
echo 100000000 > /proc/sys/fs/inotify/max_user_watches
