#1/bin/bash

echo "########################################################"
echo "# Running $1 "
echo "########################################################"

mkdir run
cp $1/* run/

python RunRichards.py

mv run/*.pkl $1/.

rm run/*
rmdir run
echo ""
