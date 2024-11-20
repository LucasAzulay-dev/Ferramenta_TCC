#include <stdio.h>
#include <string.h>
#include "instrumented_SUT.h"
extern char log_buffer[33554432];
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
void SUT()
{
  int a;
  int b;
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompA\", \"executionOrder\": \"1\", \"not_used\": {},\"in\": {\"AO1\": \"%d\",\"AO2\": \"%d\",\"AI3\": \"None\"},", AO1,AO2,AI3);
  CompA(0, 0, 0, &AO1, &AO2);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"AO1\": \"%d\",\"AO2\": \"%d\"}},", AO1,AO2);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompB\", \"executionOrder\": \"2\", \"not_used\": {},\"in\": {\"BO1\": \"%d\",\"BI2\": \"None\",\"BI3\": \"None\"},", BO1,BI2,BI3);
  CompB(0, 0, 0, &BO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"BO1\": \"%d\"}},", BO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompC\", \"executionOrder\": \"3\", \"not_used\": {},\"in\": {\"AO1\": \"%d\",\"BO1\": \"%d\",\"CO1\": \"%d\"},", AO1,BO1,CO1);
  CompC(AO1, BO1, 0, &CO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"CO1\": \"%d\"}},", CO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompE\", \"executionOrder\": \"4\", \"not_used\": {},\"in\": {\"CO1\": \"%d\"},", CO1);
  a = CompE(CO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"a\": \"%d\"}},", a);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompD\", \"executionOrder\": \"5\", \"not_used\": {},\"in\": {\"CO1\": \"%d\",\"AO2\": \"%d\"},", CO1,AO2);
  CompD(CO1, AO2, b);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"b\": \"%d\"}},", b);
}

