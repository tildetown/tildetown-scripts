#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /var/local/venvs/tildetown/bin/activate

stats=/usr/bin/stats
template=/var/www/tilde.town/template.index.html
mustache=/var/local/tildetown/scripts/mustache.hy
output_path=/var/www/tilde.town/index.html

($stats || echo '{}') | hy $mustache $template > $output_path
deactivate
