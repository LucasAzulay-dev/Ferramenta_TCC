#include <stdio.h>
void CompA(int AI1, int AI2, int AI3, int *AO1, int *AO2)
{
}

void CompB(int BI1, int BI2, int BI3, int BI4, int *BO1)
{
}

void CompC(int CI1, int CI2, int *CO1)
{
}

void CompD(int DI1, int DI2, int *DO1)
{
}

int AO1;
int AO2;
int BO1;
int CO1;
void SUT(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1)
{
  printf("Antes de CompA: SUTI1 = %d, SUTI2 = %d, SUTI3 = %d\n", SUTI1, SUTI2, SUTI3);
  CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);
  printf("Depois de CompA: AO1 = %d, AO2 = %d\n", AO1, AO2);
  printf("Antes de CompB: SUTI4 = %d, SUTI5 = %d, SUTI6 = %d, SUTI7 = %d\n", SUTI4, SUTI5, SUTI6, SUTI7);
  CompB(SUTI4, SUTI5, SUTI6, SUTI7, &BO1);
  printf("Depois de CompB: BO1 = %d\n", BO1);
  printf("Antes de CompC: AO1 = %d, BO1 = %d\n", AO1, BO1);
  CompC(AO1, BO1, &CO1);
  printf("Depois de CompC: CO1 = %d\n", CO1);
  printf("Antes de CompD: CO1 = %d, AO2 = %d, SUTO1 = %d\n", CO1, AO2, SUTO1);
  CompD(CO1, AO2, SUTO1);
}

