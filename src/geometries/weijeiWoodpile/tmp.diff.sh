#!/bin/bash
DIR=/tmp/sims/Ex

echo "Comparing files"
echo "GEO"
diff $DIR/woodpile.geo /tmp/sims/woodpile.ref.geo
echo "IN"
diff $DIR/woodpile.in /tmp/sims/woodpile.ref.in
echo "SH"
diff $DIR/woodpile.sh /tmp/sims/woodpile.ref.sh
echo "INP"
diff $DIR/woodpile.inp /tmp/sims/woodpile.ref.inp
