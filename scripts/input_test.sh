#!/bin/bash

while read -r; do
  collect="$collect / $REPLY"
done

final=$(echo $collect | sed -r 's/^.{2}//')

echo $final
