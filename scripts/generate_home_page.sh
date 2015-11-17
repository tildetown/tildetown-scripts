#!/bin/bash

# Feed JSON/tdp output from "stats" into mustache template to generate
# tilde.town homepage. Invoke periodically from crontab.

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

template=/usr/local/tildetown-scripts/tildetown/templates/frontpage.html
mustache=/usr/local/tildetown-scripts/tildetown/mustache.py
input_path=/var/www/tilde.town/tilde.json
output_path=/var/www/tilde.town/index.html

if [ ! -f "$input_path" ]; then
  print "homepage generation needs missing $input_path"
  exit 1
fi

exec /usr/local/virtualenvs/tildetown/bin/python "$mustache" "$template" < "$input_path" > "$output_path"
