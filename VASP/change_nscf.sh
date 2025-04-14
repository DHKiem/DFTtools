## current directory is band
cp ../CONTCAR ./POSCAR
cp ../INCAR .
cp ../POTCAR .
ln -s ../CHGCAR
linenumber=$(grep -n ICHARG INCAR |cut -d':' -f1)
sed -i "${linenumber}s/.*/   ICHARG = 11/g" ./INCAR
linenumber=$(grep -n NSW INCAR |cut -d':' -f1)
sed -i "${linenumber}s/.*/   NSW = 0/g" ./INCAR
linenumber=$(grep -n LCHARG INCAR |cut -d':' -f1)
sed -i "${linenumber}s/.*/   LCHARG = .FALSE./g" ./INCAR
linenumber=$(grep -n ISMEAR INCAR |cut -d':' -f1)
sed -i "${linenumber}s/.*/   ISMEAR = 0/g" ./INCAR
