#include "instrumented_SUT.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

#define BUFFER_SIZE 33554432
char log_buffer[BUFFER_SIZE];

void testeX(int num_teste, int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int SUTO1_test, long SUTO2_test);
int main(){
  int test_vecs_SUTI1[2] = {40, 0};
  int test_vecs_SUTI2[2] = {36, -10};
  int test_vecs_SUTI3[2] = {46, -1};
  int test_vecs_SUTI4[2] = {35, 30};
  int test_vecs_SUTI5[2] = {11, 40};
  int test_vecs_SUTI6[2] = {13, 50};
  int test_vecs_SUTI7[2] = {11, 60};
  int test_vecs_SUTO1[2] = {90886800, 0};
  long test_vecs_SUTO2[2] = {-1669942071, 1213825600};
  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"sutFunction\": \"SUT\",\"numberOfTests\": \"2\",  \"skipedlines\":[2, 3],\"inputs\":[\"SUTI1\", \"SUTI2\", \"SUTI3\", \"SUTI4\", \"SUTI5\", \"SUTI6\", \"SUTI7\"],\"outputs\": [\"SUTO1\", \"SUTO2\"],\"executions\": [");
    for(int i=0;i<2;i++){
            snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"testNumber\":\"%d\",\"analysis\": [",i+1);
      testeX(i, test_vecs_SUTI1[i], test_vecs_SUTI2[i], test_vecs_SUTI3[i], test_vecs_SUTI4[i], test_vecs_SUTI5[i], test_vecs_SUTI6[i], test_vecs_SUTI7[i], test_vecs_SUTO1[i], test_vecs_SUTO2[i]);
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
void testeX(int num_teste, int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int SUTO1_test, long SUTO2_test){
    int SUTO1;
    long SUTO2;
    SUT( SUTI1, SUTI2, SUTI3, SUTI4, SUTI5, SUTI6, SUTI7, &SUTO1, &SUTO2);
    if( (fabs(SUTO1 - SUTO1_test) < 0.0001) && (fabs(SUTO2 - SUTO2_test) < 0.0001) ){
       snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"true\",\"actualResult\": [\"%d\",\"%ld\"],", SUTO1, SUTO2);
      }else{
   snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"false\",\"expectedResult\": [\"%d\",\"%ld\"],\"actualResult\": [\"%d\",\"%ld\"],", SUTO1_test, SUTO2_test, SUTO1, SUTO2);
     }
}