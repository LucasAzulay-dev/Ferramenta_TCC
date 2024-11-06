#include "../src/IntegrationFunction/IntegrationFunction.h"
#include <stdio.h>

#ifdef TEST_OUT
    #define test_out 1
#else
    #define test_out 0
#endif

#define NUM_TESTES 6

void testeX(int num_teste, int SUTI[]);

int main(){
    int test_inputs[NUM_TESTES][8] = {
        {1, 1, 1, 1, 1, 1, 1, 11},
        
        // {0, 1, 1, 1, 1, 1, 1, 0},
        // {1, 0, 1, 1, 1, 1, 1, 4},
        // {1, 1, 2, 1, 1, 1, 1, 20},
        // {1, 1, 1, 4, 1, 1, 1, 23},
        // {1, 1, 1, 1, 6, 1, 1, 31},
        // {1, 1, 1, 1, 1, 7, 1, 35},
        // {1, 1, 1, 1, 1, 1, 8, 39}
        
        {1, 1, 2, 2, 1, 1, 1, 28},
        {1, 1, 2, 2, 1, 1, 1, 28},
        {1, 3, 2, 2, 1, 1, 1, 76},
        {1, 0, 2, 2, 1, 1, 1, 10},
        {1, 1, 2, 0, 1, 1, 1, 12}
    };

    for(int i=0;i<NUM_TESTES;i++){
        testeX(i+1,test_inputs[i]);
    }
    return 0;
}

void testeX(int num_teste, int SUTI[]){
    int SUTO1;
    SUT(SUTI[0], SUTI[1], SUTI[2], SUTI[3], SUTI[4], SUTI[5], SUTI[6], &SUTO1);
    if(test_out){
        if(SUTO1==SUTI[7]){
            printf("Teste %d: passou\n", num_teste);
        }else{
            printf("Teste %d: FALHOU (SUTO1=%d esperava %d)\n", num_teste, SUTO1, SUTI[7]);
        }
    }
}
