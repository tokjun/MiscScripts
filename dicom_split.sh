#! /bin/bash


for i in {12..219}
do
    DIR="Kidney2echoPETRA21MM3CRYO11000SPKFOV35GRAD9_"$i
    if [ -d $DIR ]; then
	echo "Processing "$DIR"..."
	mkdir $DIR/MAG
	mkdir $DIR/PH
	cd $DIR
	find -f *.dcm -exec sh -c 'RET=`dcmdump +P "0008,0008" $1`; if echo "$RET" | grep "M\\\NORM" >/dev/null ; then cp $1 MAG; else cp $1 PH; fi' -- {} \;
	mv MAG ../MAG_$i
	mv PH ../PH_$i
	cd ..
    fi
done
    

