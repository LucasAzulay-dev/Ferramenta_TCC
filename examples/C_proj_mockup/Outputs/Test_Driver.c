#include "instrumented_SUT.h"
#include <stdio.h>
#include <sys/time.h>
#include <string.h>

#define BUFFER_SIZE 4096
char log_buffer[BUFFER_SIZE];

void testeX(int num_teste, int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int SUTO1_test, long SUTO2_test);
int main(){
  struct timeval begin, end;
  int test_vecs_SUTI1[4] = {40, 40, 35, 0};
  int test_vecs_SUTI2[4] = {36, 34, 30, -10};
  int test_vecs_SUTI3[4] = {46, 34, 25, -1};
  int test_vecs_SUTI4[4] = {1, 1, 12, 30};
  int test_vecs_SUTI5[4] = {11, 11, 11, 40};
  int test_vecs_SUTI6[4] = {13, 13, 13, 50};
  int test_vecs_SUTI7[4] = {11, 11, 11, 60};
  int test_vecs_SUTO1[4] = {4, 3, 2, 2};
  long test_vecs_SUTO2[4] = {1, 2, 3, 4};
  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"sutFunction\": \"SUT\",\"numberOfTests\": 4,  \"skipedlines\":[],\"inputs\":[\"SUTI1\", \"SUTI2\", \"SUTI3\", \"SUTI4\", \"SUTI5\", \"SUTI6\", \"SUTI7\"],\"outputs\": [\"SUTO1\", \"SUTO2\"],\"executions\": [");
    for(int i=0;i<4;i++){
            snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"{\"testNumber\":%d,\"analysis\": [",i+1);
         gettimeofday(&begin,NULL);
      testeX(i, test_vecs_SUTI1[i], test_vecs_SUTI2[i], test_vecs_SUTI3[i], test_vecs_SUTI4[i], test_vecs_SUTI5[i], test_vecs_SUTI6[i], test_vecs_SUTI7[i], test_vecs_SUTO1[i], test_vecs_SUTO2[i]);
        gettimeofday(&end,NULL);
          int elapsed = (((end.tv_sec - begin.tv_sec) * 1000000) + (end.tv_usec - begin.tv_usec))/4;
         snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"\"executionTime\": %d},",elapsed);
     }
  snprintf(log_buffer + strlen(log_buffer),BUFFER_SIZE - strlen(log_buffer),"],}"); 
  printf("%s", log_buffer);
return 0;
}
void testeX(int num_teste, int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int SUTO1_test, long SUTO2_test){
    int SUTO1;
    long SUTO2;
    SUT( SUTI1, SUTI2, SUTI3, SUTI4, SUTI5, SUTI6, SUTI7, &SUTO1, &SUTO2);
    if( SUTO1 == SUTO1_test && SUTO2 == SUTO2_test ){
       snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"true\",");
      }else{
   snprintf(log_buffer + strlen(log_buffer), BUFFER_SIZE - strlen(log_buffer), "],\"pass\": \"false\",\"expectedResult\": [%d,%ld],\"actualResult\": [%d,%ld],", SUTO1_test, SUTO2_test, SUTO1, SUTO2);
     }
}