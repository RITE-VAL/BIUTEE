#!/bin/sh

ls FV/my/*.raw | parallel "./make_sub_zunder.sh {} 1 > {.}.cab_zunda" &

ls SV/my/*.raw | parallel "./make_sub_zunder.sh {} > {.}.cab_zunda" &
