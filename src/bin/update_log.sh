#!/bin/bash
(find -L $HOME -name "*.sh" | xargs getDataState.sh ) >$HOME/fdtd_status.log
