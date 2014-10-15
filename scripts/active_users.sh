#!/bin/bash
who | cut -d' ' -f1 | sort -u | wc -l
