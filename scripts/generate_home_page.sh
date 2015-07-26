#!/bin/bash

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

source /var/local/venvs/tildetown/bin/activate

stats=/usr/local/bin/generate_stats
template=/var/www/tilde.town/template.index.html
mustache=/var/local/tildetown/scripts/mustache.hy
output_path=/var/www/tilde.town/index.html

# hello from datagrok
#
# generate_stats was breaking and outputting no lines. i dunno how to fix that,
# but i can un-disaappear the homepage by saying "output empty json if broken"
#
# generate_stats | hy $mustache $template > $output_path
($stats || echo '{}') | hy $mustache $template > $output_path
