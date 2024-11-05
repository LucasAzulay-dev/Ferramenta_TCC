#include <stdio.h>
#include <string.h>
extern char log_buffer[4096];
void CompA(int AI1, int AI2, int AI3, int *AO1, int *AO2)
{
  *AO1 = AI1 + AI2;
  *AO2 = AI1 * AI3;
}

void CompB(int BI1, int BI2, int BI3, int *BO1)
{
  *BO1 = (BI1 + BI2) * BI3;
}

void CompC(int CI1, int CI2, int CI3, int *CO1)
{
  *CO1 = ((CI1 + CI2) * CI1) + CI3;
}

long CompE(int value)
{
  return value * ((long) value);
}

void CompD(int DI1, int DI2, int *DO1)
{
  *DO1 = (DI1 - DI2) * DI2;
}

int AO1;
int AO2;
int BO1;
int CO1;
void SUT(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1, long *SUTO2)
{
  CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompA\", \"executionOrder\": \"1\", \"in\": {\"SUTI1\": \"%d\",\"SUTI2\": \"%d\",\"SUTI3\": \"%d\"}, \"out\": {\"AO1\": \"%d\",\"AO2\": \"%d\"}},\n",SUTI1,SUTI2,SUTI3,AO1,AO2);
  CompB(SUTI4, SUTI5, SUTI6, &BO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompB\", \"executionOrder\": \"2\", \"in\": {\"SUTI4\": \"%d\",\"SUTI5\": \"%d\",\"SUTI6\": \"%d\"}, \"out\": {\"BO1\": \"%d\"}},\n",SUTI4,SUTI5,SUTI6,BO1);
  CompC(AO1, BO1, SUTI7, &CO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompC\", \"executionOrder\": \"3\", \"in\": {\"AO1\": \"%d\",\"BO1\": \"%d\",\"SUTI7\": \"%d\"}, \"out\": {\"CO1\": \"%d\"}},\n",AO1,BO1,SUTI7,CO1);
  *SUTO2 = CompE(CO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompE\", \"executionOrder\": \"4\", \"in\": {\"CO1\": \"%d\"}, \"out\": {\"SUTO2\": \"%ld\"}},\n",CO1,*SUTO2);
  CompD(CO1, AO2, SUTO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompD\", \"executionOrder\": \"5\", \"in\": {\"CO1\": \"%d\",\"AO2\": \"%d\"}, \"out\": {\"SUTO1\": \"%d\"}},\n",CO1,AO2,*SUTO1);
}

