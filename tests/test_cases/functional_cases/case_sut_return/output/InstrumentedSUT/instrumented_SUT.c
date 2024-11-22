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

void CompD(int DI1, int DI2, int *DO1)
{
  *DO1 = (DI1 - DI2) * DI2;
}

long CompE(int value)
{
  return value * ((long) value);
}

int CompF(int value)
{
  return value + 1;
}

int AO1;
int AO2;
int BO1;
int CO1;
int teste_return;
int sut(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1, long *SUTO2)
{
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompA\", \"executionOrder\": \"1\", \"not_used\": {},\"in\": {\"SUTI1\": \"%d\",\"SUTI2\": \"%d\",\"SUTI3\": \"%d\"},", SUTI1,SUTI2,SUTI3);
  CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"AO1\": \"%d\",\"AO2\": \"%d\"}},", AO1,AO2);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompB\", \"executionOrder\": \"2\", \"not_used\": {},\"in\": {\"SUTI4\": \"%d\",\"SUTI5\": \"%d\",\"SUTI6\": \"%d\"},", SUTI4,SUTI5,SUTI6);
  CompB(SUTI4, SUTI5, SUTI6, &BO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"BO1\": \"%d\"}},", BO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompC\", \"executionOrder\": \"3\", \"not_used\": {},\"in\": {\"AO1\": \"%d\",\"BO1\": \"%d\",\"SUTI7\": \"%d\"},", AO1,BO1,SUTI7);
  CompC(AO1, BO1, SUTI7, &CO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"CO1\": \"%d\"}},", CO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompD\", \"executionOrder\": \"4\", \"not_used\": {},\"in\": {\"CO1\": \"%d\",\"AO2\": \"%d\"},", CO1,AO2);
  CompD(CO1, AO2, SUTO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"SUTO1\": \"%d\"}},", *SUTO1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompE\", \"executionOrder\": \"5\", \"not_used\": {},\"in\": {\"CO1\": \"%d\"},", CO1);
  *SUTO2 = CompE(CO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"SUTO2\": \"%ld\"}},", *SUTO2);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"CompF\", \"executionOrder\": \"6\", \"not_used\": {},\"in\": {\"CO1\": \"%d\"},", CO1);
  teste_return = CompF(CO1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"teste_return\": \"%d\"}},", teste_return);
  return teste_return;
}

