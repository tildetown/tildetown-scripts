#!/bin/bash
who | cut -d' ' -f1 | sort -u | wc -l | xargs echo "active_user_count=" | sed 's/ //'
