#!/bin/bash
# remove files generated by bristol FDTD
# TODO: Try replacing find string with variable, use flags, etc. Pythonify and argparse?
# TODO: remove torque output: "*.e4805897" and "*.o4805897" (need regex matching power...)

function findBFDTDoutput
{
  find . -type f \( -name "*.h5" -o -name "*.prn" -o -name "*.out" -o -name "geom.geo" -o -name "namiki.txt" -o -name "*.int" -o -name "heat.txt" -o -name "lumped.log" -o -name "time*.txt" -o -name "e*.txt" -o -name "*.sh.e*" -o -name "*.sh.o*" -o -name "debug.txt" -o -name "from_rotated.geo" -o -name "geom_info.txt" -o -name "netgen.geo" -o -name "snap_info.txt" -o -name "snapstrp.geo" \) $*
}
#alias findBFDTDoutput='find . -type f \( -name "*.prn" -o -name "*.out" -o -name "geom.geo" -o -name "namiki.txt" -o -name "*.int" -o -name "heat.txt" -o -name "lumped.log" -o -name "time*.txt" -o -name "e*.txt" \)'

ORIGDIR=$(pwd)

ans="none"

for DIR in "$@"
do
	cd ${ORIGDIR}
	cd ${DIR}

	if [[ ${ans} != 'all' ]]
	then
		findBFDTDoutput | less
		echo "Remove those object files? (y=directly, i=interactively, all=yes for all, *=exit)"
		read ans
	fi
	case ${ans} in
	  y|Y|yes|all) findBFDTDoutput -exec rm -v {} \; ;;
	  i|I)     findBFDTDoutput -exec rm -iv {} \; ;;
	  *)       exit 1;;
	esac
done

cd ${ORIGDIR}
