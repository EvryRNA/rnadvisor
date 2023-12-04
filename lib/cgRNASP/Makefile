install_all:
	mkdir -p bin
	gcc cgRNASP/cgRNASP.c -lm -o bin/cgRNASP_bin 
	gcc cgRNASP-C/cgRNASP-C.c -lm -o bin/cgRNASP-C_bin 
	gcc cgRNASP-PC/cgRNASP-PC.c -lm -o bin/cgRNASP-PC_bin 
	cp -r cgRNASP/data bin/cgRNASP_data
	cp -r cgRNASP-C/data bin/cgRNASP-C_data
	cp -r cgRNASP-PC/data bin/cgRNASP-PC_data

