#!/bin/bash
RUNNING=$(qstat | grep $USER | grep " R " | wc -l)
QUEUED=$(qstat | grep $USER | grep " Q " | wc -l)
TOTAL=$(qstat | grep $USER | wc -l)
echo "job stats: running=$RUNNING queued=$QUEUED total=$TOTAL"
