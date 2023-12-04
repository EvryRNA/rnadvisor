# cgRNASP

Coarse-grained statistical potential involving three CG beads at P, C4’, and N9 atoms for purine (or N1 atom for pyrimidine).

# Compilation and usage under linux

```
# Compilation

 gcc cgRNASP.c -lm -o cgRNASP

# An example usage in the “example” dir

 N=`ls *.pdb | wc -l`
 ./cgRNASP ./ ${N} energy_list.txt

 Output:
   
  2_bujnicki_1_rpr.pdb     -715.410964 kBT
  4_adamiak_1_rpr.pdb     -909.539651 kBT

Note: the subfolder "data/" and compiled "cgRNASP" should be in the same folder.
Please feel free to contact us if you have any question! zjtan@whu.edu.cn
```

