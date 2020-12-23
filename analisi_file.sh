#real    1m13.548s                                                                                                                                                                           #user    0m52.533s                                                                                                                                                                           #sys     0m55.020s 

find . -path "*/Station_?__??/Station_?__??_Summary/Chip_???/S_curve/Ch_?_offset_?_Chip_???.txt" >> file_path.txt;

number='[+-]?[0-9]+\.?[0-9]*';
while IFS= read -r line
do
	primariga=$(head -1 $line | cut -d " " -f 1 );
	if [[ $primariga =~ $number ]]; then
		echo $line,$primariga >> elenco_file_temporaneo.txt;
	fi
done < file_path.txt
sed -e 's/[^-?0-9]/ /g' elenco_file_temporaneo.txt | awk -F ' ' '{print $4,$5,$6,$7,$8,$12 "." $13,$14 "." $15}' >> valori.txt;
#rm elenco_file_temporaneo.txt;


