#include <stdio.h>
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
  printf("sut_output_variables_and_initial_values: [{SUTO1:%d, SUTO2:%ld}}]\n", *SUTO1, *SUTO2);
  printf("CompA_return_variables_and_initial_values: [{SUTI1:%d, SUTI2:%d, SUTI3:%d}}]\n", SUTI1, SUTI2, SUTI3);
  CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);
  printf("CompA_return_variables_and_final_values: [{AO1:%d, AO2:%d}}]\n", AO1, AO2);
  printf("CompB_return_variables_and_initial_values: [{SUTI4:%d, SUTI5:%d, SUTI6:%d}}]\n", SUTI4, SUTI5, SUTI6);
  CompB(SUTI4, SUTI5, SUTI6, &BO1);
  printf("CompB_return_variables_and_final_values: [{BO1:%d}}]\n", BO1);
  printf("CompC_return_variables_and_initial_values: [{AO1:%d, BO1:%d, SUTI7:%d}}]\n", AO1, BO1, SUTI7);
  CompC(AO1, BO1, SUTI7, &CO1);
  printf("CompC_return_variables_and_final_values: [{CO1:%d}}]\n", CO1);
  printf("CompE_return_variables_and_initial_values: [{CO1:%d}}]\n", CO1);
  *SUTO2 = CompE(CO1);
  printf("CompD_return_variables_and_initial_values: [{CO1:%d, AO2:%d}}]\n", CO1, AO2);
  CompD(CO1, AO2, SUTO1);
  printf("sut_output_variables_and_final_values: [{SUTO1:%d, SUTO2:%ld}}]\n", *SUTO1, *SUTO2);
}

int main()
{
    int SUTO1 = 0;
    long SUTO2 = 0;
    SUT(1, 2, 3, 4, 5, 6, 7, &SUTO1, &SUTO2);
    return 0;
}
