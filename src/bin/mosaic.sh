#!/bin/bash
set -eux
convert $1 \( $2 $3 -append \) -gravity center +append $4
