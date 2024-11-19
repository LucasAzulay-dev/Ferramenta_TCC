#include "instrumented_SUT.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

#define BUFFER_SIZE 33554432
char log_buffer[BUFFER_SIZE];

void testeX(int num_teste, int SUTI1, float SUTI2, int SUTI3, int SUTO1_test, int SUTO2_test, float SUTO3_test);
int main(){
  int test_vecs_SUTI1[7] = {0, 1, 1, 1, 1, 1, 1};
  float test_vecs_SUTI2[7] = {0, 1, 1, 1, 1, 2, 2};
  int test_vecs_SUTI3[7] = {0, -1, -1, 2, 2, 2, 2};
  int test_vecs_SUTO1[7] = {0, 0, 0, 0, 0, 0, 0};
  int test_vecs_SUTO2[7] = {0, 0, 0, 3, 3, 1, 1};
  float test_vecs_SUTO3[7] = {-470.090, -470.090, -470.090, -470.090, -470.090, 30.400, 30.400};
  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"sutFunction\": \"sut\",\"numberOfTests\": \"7\",  \"skipedlines\":[],\"inputs\":[\"i1\", \"i2\", \"i3\"],\"outputs\": [\"o1\", \"o2\", \"o3\"],\"executions\": [");
    for(int i=0;i<7;i++){
            snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"testNumber\":\"%d\",\"analysis\": [",i+1);
      testeX(i, test_vecs_SUTI1[i], test_vecs_SUTI2[i], test_vecs_SUTI3[i], test_vecs_SUTO1[i], test_vecs_SUTO2[i], test_vecs_SUTO3[i]);
    int elapsed = 0;
        snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"\"executionTime\": \"%d\"},",elapsed);
     }
  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"],}"); 
printf("%s", log_buffer);
  FILE *arquivo;
  fopen_s(&arquivo,"output/OutputBuffer/log_buffer.txt", "w");
  fputs(log_buffer, arquivo);
  fputs("\n\n", arquivo);
  fclose(arquivo);
return 0;
}
void testeX(int num_teste, int SUTI1, float SUTI2, int SUTI3, int SUTO1_test, int SUTO2_test, float SUTO3_test){
    int SUTO1;
    int SUTO2;
    float SUTO3;
    sut( SUTI1, SUTI2, SUTI3, &SUTO1, &SUTO2, &SUTO3);
    if( (fabs(SUTO1 - SUTO1_test) < 0.0001) && (fabs(SUTO2 - SUTO2_test) < 0.0001) && (fabs(SUTO3 - SUTO3_test) < 0.0001) ){
       snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"true\",\"actualResult\": [\"%d\",\"%d\",\"%.3f\"],", SUTO1, SUTO2, SUTO3);
      }else{
   snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"false\",\"expectedResult\": [\"%d\",\"%d\",\"%.3f\"],\"actualResult\": [\"%d\",\"%d\",\"%.3f\"],", SUTO1_test, SUTO2_test, SUTO3_test, SUTO1, SUTO2, SUTO3);
     }
}