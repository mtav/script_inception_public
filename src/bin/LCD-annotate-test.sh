#!/bin/bash
set -eu
IN="no8_2500.jpg"
TXT="25.00°C"
OUT="a_test.jpg"

echo $LINENO
convert ${IN}   -background Khaki  label:"${TXT}" \
          -gravity Center -append    anno_label.jpg
          
echo $LINENO
convert ${IN}   -background Orange  label:"${TXT}" \
          +swap  -gravity Center -append    anno_label2.jpg
          
echo $LINENO
convert ${IN} \
          -gravity South   -background Plum   -splice 0x18 \
          -annotate +0+2 "${TXT}"   anno_splice.gif
echo $LINENO
convert ${IN} \
          -gravity North   -background YellowGreen  -splice 0x18 \
          -annotate +0+2 "${TXT}"   anno_splice2.gif

echo $LINENO
montage -label "${TXT}"  ${IN} \
          -geometry +0+0 -background Gold anno_montage.jpg

echo $LINENO
montage -label "${TXT}" ${IN} \
          -font Candice -pointsize 15 \
          -frame 5  -geometry +0+0 anno_montage2.jpg

echo $LINENO
convert -caption "${TXT}" ${IN} -gravity center \
           -background black +polaroid anno_polaroid.png

echo $LINENO
convert ${IN} -gravity south \
          -stroke '#000C' -strokewidth 2 -annotate 0 "${TXT}" \
          -stroke  none   -fill white    -annotate 0 "${TXT}" \
          anno_outline.jpg
          
echo $LINENO
convert ${IN} \
          -fill '#0008' -draw 'rectangle 5,128,114,145' \
          -fill white   -annotate +10+141 "${TXT}" \
          anno_dim_draw.jpg

echo $LINENO
convert ${IN}  -fill white  -undercolor '#00000080'  -gravity South \
          -annotate +0+5 "${TXT}"     anno_undercolor.jpg

echo $LINENO
convert -background '#00000080' -fill white label:"${TXT}" miff:- |\
  composite -gravity south -geometry +0+3 \
              -   ${IN}   anno_composite.jpg
         
echo $LINENO
width=`identify -format %w ${IN}`; \
convert -background '#0008' -fill white -gravity center -size ${width}x100 \
          caption:"${TXT}" \
          ${IN} +swap -gravity south -composite  anno_caption.jpg
       
echo $LINENO
convert -size 100x14 xc:none -gravity center \
          -stroke black -strokewidth 2 -annotate 0 "${TXT}" \
          -background none -shadow 100x3+0+0 +repage \
          -stroke none -fill white     -annotate 0 "${TXT}" \
          ${IN}  +swap -gravity south -geometry +0-3 \
          -composite  anno_fancy.jpg
