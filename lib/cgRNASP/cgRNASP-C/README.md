# cgRNASP-C

Coarse-grained statistical potential involving one CG bead at C4’.

# Compilation and usage under linux

```
# Compilation

 gcc cgRNASP-C.c -lm -o cgRNASP-C

# An example usage in the “example” dir

 N=`ls *.pdb | wc -l`
 ./cgRNASP-C ./ ${N} energy_list.txt

 Output:
   
  2_bujnicki_1_rpr.pdb     -1309.032031 kBT
  4_adamiak_1_rpr.pdb     -1673.517967 kBT

Note: the subfolder "data/" and compiled "cgRNASP-C" should be in the same folder.
Please feel free to contact us if you have any question! zjtan@whu.edu.cn
```
