#include "SUT.h"
#include <stdio.h>
#include <sys/time.h>
void testeX(int num_teste, int SUTI[]);
int main(){
    struct timeval begin, end;
   int test_inputs[4][8] = {

        {40,36,46,1,11,13,11,4},
        {40,34,34,1,11,13,11,3},
        {35,30,25,12,11,13,11,2},
        {0,-10,-1,30,40,50,60,2}
    };
gettimeofday(&begin,NULL);
 for(int i=0;i<4;i++){
    testeX(i+1,test_inputs[i]);
   }
gettimeofday(&end,NULL);
int elapsed = (((end.tv_sec - begin.tv_sec) * 1000000) + (end.tv_usec - begin.tv_usec))/4;
printf("Execution time: %d micro seconds\n",elapsed);
 return 0;
}
void testeX(int num_teste, int SUTI[]){
    int SUTO1;
    SUT(SUTI[0], SUTI[1], SUTI[2], SUTI[3], SUTI[4], SUTI[5], SUTI[6],  &SUTO1);
    if( SUTO1==SUTI[7] ){
       printf("Teste %d : PASSOU\n", num_teste);
      }else{
        printf("Teste %d: FALHOU\n", num_teste);
     }
}