sqlplus -S guest/password @CRTall

tables=( state mass dorm major minor )
for i in "${tables[@]}"
do
    echo "*** Loading $i.csv...***"
    sqlldr guest/password "control=LOAD$i.ctl" SILENT=HEADER LOG="./logs/LOAD$i.log"
    echo ""
done
