#include<stdio.h>
#include<math.h>
#include<dirent.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<time.h>
#include<string.h>
#include<stdlib.h>

double ***read_potential(char potential_file[], int intervals)
{
 int i, j;
 double ***p=(double ***)malloc(4*sizeof(double**));

 for(i=0;i<4;i++) 
  p[i]=(double **)malloc(4*sizeof(double*));
 
 for(i=0;i<4;i++)
  for(j=0;j<4;j++)
   p[i][j]=(double *)malloc(intervals*sizeof(double));

 FILE *p_f;
 int n1, n2, n3, nnn;

 p_f=fopen(potential_file,"r+");
 while(!feof(p_f))
 {
  for(n1=0;n1<4;n1++)
   for(n2=0;n2<4;n2++)
    for(n3=0;n3<intervals;n3++)
     fscanf(p_f,"%d %d %d %lf\n",&nnn,&nnn,&nnn,&p[n1][n2][n3]);
 }
 fclose(p_f);

 if(intervals != n3)
 {
  printf("Error---loading_potential---Error!\n");
  exit(-1);          
 }
 return p;
}

int open_dir(char file_name[][300], char file_name1[][300], char route[])
{
  DIR *dir;
  struct dirent *ptr;
  int k=0;
  char *c;

  dir=opendir(route);

  while((ptr=readdir(dir))!=NULL)
  {
    c=ptr->d_name;
    while(*c!='\0')
     c++;

   if(strcmp((c-4),".pdb")==0 && strcmp((c-7),".pdb")!=0)
   {
    sprintf(file_name[k],"%s",ptr->d_name);
    sprintf(file_name1[k],"%s/%s",route,ptr->d_name);
    k++;
   }
  }
   closedir(dir);
   return k;
}

int read_pdb(char pdb_file[300], char type1[][5], char type2[][5], char type[][10], char chain[][5], char num[][10], float x[], float y[], float z[], int L)
{
 FILE *pdb_f;
 char aline[500], x1[L][10], y1[L][10], z1[L][10];
 int i, cc1, cc2, lll;

 pdb_f=fopen(pdb_file,"r+");
 
 i=0;
 memset(x1, 0, sizeof(x1));
 memset(y1, 0, sizeof(y1));
 memset(z1, 0, sizeof(z1));
 while(fgets(aline,500,pdb_f)!=NULL)
 {
  if(aline[0]=='A' && aline[1]=='T' && aline[2]=='O' && aline[3]=='M')
  {
   sprintf(type1[i],"%c%c%c",aline[13],aline[14],aline[15]);//atom_type
   if(type1[i][0]==' ')
    for(cc1=1;cc1<strlen(type1[i]);cc1++)
     if(type1[i][cc1]!=' ')
     {
      for(cc2=cc1;cc2<strlen(type1[i]);cc2++)
       type1[i][cc2-cc1]=type1[i][cc2];
      type1[i][cc2-1]='\0';
      break;
     }
   sprintf(type2[i],"%c",aline[19]);//residue_type
   sprintf(chain[i],"%c",aline[21]);//chain_type

   sprintf(num[i],"%c%c%c%c",aline[22],aline[23],aline[24],aline[25]);//residue_number
   sprintf(x1[i],"%c%c%c%c%c%c%c%c",aline[30],aline[31],aline[32],aline[33],aline[34],aline[35],aline[36],aline[37]);//x_coordinate
   x[i]=atof(x1[i]);
   sprintf(y1[i],"%c%c%c%c%c%c%c%c",aline[38],aline[39],aline[40],aline[41],aline[42],aline[43],aline[44],aline[45]);//y_coordinate
   y[i]=atof(y1[i]);
   sprintf(z1[i],"%c%c%c%c%c%c%c%c",aline[46],aline[47],aline[48],aline[49],aline[50],aline[51],aline[52],aline[53]);//z_coordinate
   z[i]=atof(z1[i]);

   sprintf(type[i],"%s%s",type2[i],type1[i]);
   for(lll=0;lll<strlen(type[i]);lll++)
    if(type[i][lll]==' ')
     type[i][lll]='\0';

   i++;
  }
  memset(aline,0,sizeof(aline));
 }
 fclose(pdb_f);
 return i;
}

double fun(int n)
{
 return -175.0/sqrt(n+39) + 27.0;
}

int main(int argc, char *argv[])
{
 clock_t start,end;
 start=clock();

 float spendtime;

 int k1, k2, k3, k4, intervals1, intervals2, intervals3, intervals4, iii;
 double Rc1, Rc2, Rc3, Rc4;
 k1=0; k2=1; k3=2; k4=4;
 Rc1=7.0; Rc2=12.0; Rc3=16.0; Rc4=24.0;
 intervals1=23; intervals2=40; intervals3=53; intervals4=80;

//atomtype
/////////////////////////////////////////////////////////
 char atomtype[4][6];
 FILE *atom_type;
 iii=0;
 memset(atomtype,0,sizeof(atomtype));
 atom_type=fopen("lib/cgRNASP/bin/cgRNASP-C_data/4atom_type.dat","r+");
 while(!feof(atom_type))
 {
  fscanf(atom_type,"%s\n",atomtype[iii]);
  iii++;
 }
 fclose(atom_type);

//restype
 char restype[4][2]={"A", "U", "C", "G"};

 int n33, n44, nums[4], nume[4];
 nums[0]=0; nume[0]=1;
 nums[1]=1; nume[1]=2;
 nums[2]=2; nume[2]=3;
 nums[3]=3; nume[3]=4;

/////////////////////////////////////////////////////////
//potential
/////////////////////////////////////////////////////////
 double ***potential1, ***potential2, ***potential3, ***potential4;
 potential1 = read_potential("lib/cgRNASP/bin/cgRNASP-C_data/0-1_short-ranged.potential", intervals1);
 potential2 = read_potential("lib/cgRNASP/bin/cgRNASP-C_data/1-2_short-ranged.potential", intervals2);
 potential3 = read_potential("lib/cgRNASP/bin/cgRNASP-C_data/2-4_short-ranged.potential", intervals3);
 potential4 = read_potential("lib/cgRNASP/bin/cgRNASP-C_data/long-ranged.potential", intervals4);
/////////////////////////////////////////////////////////

//read_pdb
/////////////////////////////////////////////////////////
 FILE *pdb_f, *FP;
 int n1, n2, n3, n4, nnn, NNN, length, Len, number;
// number=atoi(argv[2]);
 char aline[500], file_name[number][300], file_name1[number][300];
 double distance, energy, energy1, energy2, energy3, energy4;

// memset(file_name,0,sizeof(file_name));
// memset(file_name1,0,sizeof(file_name1));
// NNN=open_dir(file_name, file_name1, argv[1]);

// FP = fopen(argv[3],"w+");

// for(nnn=0;nnn<NNN;nnn++)
// {
 pdb_f=fopen(argv[1],"r+");
 Len=0;
 memset(aline,0,sizeof(aline));
 while(fgets(aline,500,pdb_f)!=NULL)
 {
  Len++;
  memset(aline,0,sizeof(aline));
 }
 fclose(pdb_f);

 int N;
 char type1[Len][5], type2[Len][5], type[Len][10], chain[Len][5], num[Len][10];
 float x[Len], y[Len], z[Len];
 memset(type1,0,sizeof(type1)); memset(type2,0,sizeof(type2)); memset(type,0,sizeof(type));
 memset(chain,0,sizeof(chain));
 memset(num,0,sizeof(num));
 memset(x,0,sizeof(x)); memset(y,0,sizeof(y)); memset(z,0,sizeof(z));

 N=read_pdb(argv[1], type1, type2, type, chain, num, x, y, z, Len);
/////////////////////////////////////////////////////////
//obtainig_energy
/////////////////////////////////////////////////////////

 energy=0.0; energy1=0.0; energy2=0.0; energy3=0.0; energy4=0.0;
 for(n1=0;n1<N;n1++)
  for(n2=n1+1;n2<N;n2++)
   if(strcmp(num[n1], num[n2])!=0 || strcmp(chain[n1], chain[n2])!=0)
    for(n33=0;n33<4;n33++)
     if(strcmp(type2[n1],restype[n33])==0)
     {
      for(n3=nums[n33];n3<nume[n33];n3++)
       if(strcmp(type[n1],atomtype[n3])==0)
       {
        for(n44=0;n44<4;n44++)
         if(strcmp(type2[n2],restype[n44])==0)
         {
          for(n4=nums[n44];n4<nume[n44];n4++)
           if(strcmp(type[n2],atomtype[n4])==0)
           {
            distance=sqrt((x[n1]-x[n2])*(x[n1]-x[n2])+(y[n1]-y[n2])*(y[n1]-y[n2])+(z[n1]-z[n2])*(z[n1]-z[n2]));
///
            if(abs(atoi(num[n1])-atoi(num[n2]))>k4 || strcmp(chain[n1], chain[n2])!=0)//long-ranged
            {
             //if(distance>0 && distance<=Rc4)
             if((int)(distance/0.3)<intervals4)
              energy4+=potential4[n3][n4][(int)(distance/0.3)];
            }
///
///
             else if(abs(atoi(num[n1])-atoi(num[n2]))>k1 && abs(atoi(num[n1])-atoi(num[n2]))<=k2 && strcmp(chain[n1], chain[n2])==0)//short-ranged
            {
             //if(distance>0 && distance<=Rc1)
            if((int)(distance/0.3)<intervals1)
             energy1+=potential1[n3][n4][(int)(distance/0.3)];
            }
///
///
            else if(abs(atoi(num[n1])-atoi(num[n2]))>k2 && abs(atoi(num[n1])-atoi(num[n2]))<=k3 && strcmp(chain[n1], chain[n2])==0)//short-ranged
           {
            //if(distance>0 && distance<=Rc2)
            if((int)(distance/0.3)<intervals2)
             energy2+=potential2[n3][n4][(int)(distance/0.3)];
           }
///
           else if(abs(atoi(num[n1])-atoi(num[n2]))>k3 && abs(atoi(num[n1])-atoi(num[n2]))<=k4 && strcmp(chain[n1], chain[n2])==0)//short-ranged
           {
            //if(distance>0 && distance<=Rc3)
            if((int)(distance/0.3)<intervals3)
             energy3+=potential3[n3][n4][(int)(distance/0.3)];
           }
///
          break;
         }
        break;
       }
      break;
     }
    break;
   }

 length=1;
 for(n1=0;n1<N-1;n1++)
  if(strcmp(type2[n1],type2[n1+1])!=0 || strcmp(num[n1],num[n1+1])!=0 || strcmp(chain[n1],chain[n1+1])!=0)
   length++;

 energy = 1.0*energy1 + 3.7*energy2 + 5.0*energy3 + 42.5*energy4/fun(length);

 printf("%lf\n", energy);
// }
// fclose(FP);
/////////////////////////////////////////////////////////

  int i, j;
  for(i=0;i<4;i++)
   for(j=0;j<4;j++)
    free(potential1[i][j]);
  for(i=0;i<4;i++)
   free(potential1[i]);
  free(potential1);

  for(i=0;i<4;i++)
   for(j=0;j<4;j++)
    free(potential2[i][j]);
  for(i=0;i<4;i++)
   free(potential2[i]);
  free(potential2);

  for(i=0;i<4;i++)
   for(j=0;j<4;j++)
    free(potential3[i][j]);
  for(i=0;i<4;i++)
   free(potential3[i]);
  free(potential3);

  for(i=0;i<4;i++)
   for(j=0;j<4;j++)
    free(potential4[i][j]);
  for(i=0;i<4;i++)
   free(potential4[i]);
  free(potential4);

  end = clock();
  spendtime = (float)(end-start)/(CLOCKS_PER_SEC);

  return 0;
}



