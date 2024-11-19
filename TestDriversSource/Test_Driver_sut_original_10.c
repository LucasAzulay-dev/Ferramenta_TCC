#include "sut.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

#define BUFFER_SIZE 33554432
char log_buffer[BUFFER_SIZE];

void testeX(int SUTI1, float SUTI2, int SUTI3, int SUTO1_test, int SUTO2_test, float SUTO3_test);
int main(){
  int test_vecs_SUTI1[10] = {5, 5, 5, 5, 5, 5, 5, 5, 5, 5};
  float test_vecs_SUTI2[10] = {-1, -1, -1, -1, 1, 1, 1, 1, 1, -1};
  int test_vecs_SUTI3[10] = {1000, 1000, 999, 1001, 1000, 1000, 999, 1001, 1001, 1000};
  int test_vecs_SUTO1[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  int test_vecs_SUTO2[10] = {999, 999, 998, 1000, 1001, 1001, 1000, 1002, 1002, 999};
  float test_vecs_SUTO3[10] = {20912.699, 20912.699, -470.090, -470.090, -470.090, -470.090, -470.090, -470.090, -470.090, 20912.699};
  for(int i=0;i<10;i++){
  testeX(test_vecs_SUTI1[i], test_vecs_SUTI2[i], test_vecs_SUTI3[i], test_vecs_SUTO1[i], test_vecs_SUTO2[i], test_vecs_SUTO3[i]);
  }
return 0;
}
void testeX(int SUTI1, float SUTI2, int SUTI3, int SUTO1_test, int SUTO2_test, float SUTO3_test){
    sut( SUTI1, SUTI2, SUTI3, &SUTO1_test, &SUTO2_test, &SUTO3_test);
}