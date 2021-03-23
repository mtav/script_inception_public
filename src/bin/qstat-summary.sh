#!/bin/bash
Ntotal=$(qstat -u $USER | grep -c $USER);
Nrunning=$(qstat -u $USER | grep $USER | grep -c " R ");
Nqueued=$(qstat -u $USER | grep $USER | grep -c " Q ");
echo "job status: running = ${Nrunning} queued = ${Nqueued} total = ${Ntotal}"
