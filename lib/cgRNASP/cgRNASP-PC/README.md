# cgRNASP-PC

Coarse-grained statistical potential involving two CG beads at P, C4’.

# Compilation and usage under linux

```
# Compilation

gcc cgRNASP-PC.c -lm -o cgRNASP-PC

# An example usage in the “example” dir

 N=`ls *.pdb | wc -l`
 ./cgRNASP-PC ./ ${N} energy_list.txt

 Output:
   
  2_bujnicki_1_rpr.pdb     -388.989957 kBT
  4_adamiak_1_rpr.pdb     -542.125408 kBT

Note: the subfolder "data/" and compiled "cgRNASP-PC" should be in the same folder.
Please feel free to contact us if you have any question! zjtan@whu.edu.cn
```
