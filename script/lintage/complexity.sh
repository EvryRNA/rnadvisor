#!/bin/bash


score=$( $PYTHON radon cc ${PATH_TO_CODE}  --total-average | tail -n1 | awk '{print $4}' | sed 's/(//' | sed 's/)//')
echo "SCORE : ${score} | Acceptable score : ${COMPLEXITY_SCORE}"
condition=`echo "$score<=$COMPLEXITY_SCORE" | bc -l`
if [[ $condition == "1" ]]; then
  echo "SCORE ACCEPTABLE"
  exit 0
else
  echo "SCORE NOT ACCETABLE"
  exit 1
fi