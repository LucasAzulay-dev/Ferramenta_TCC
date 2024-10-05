// # include "./CompA/CompA.h"
// # include "./CompB/CompB.h"
// # include "./CompC/CompC.h"
// # include "./CompD/CompD.h"
#include <stdio.h>

void CompA(int AI1, int AI2, int AI3, int *AO1, int *AO2)
{
    *AO1 = AI1 + AI2;
    *AO2 = AI1 * AI3;
}

void CompB(int BI1, int BI2, int BI3, int *BO1)
{
    *BO1 = (BI1 + BI2) * (BI3);
}

void CompC(int CI1, int CI2, int CI3, int *CO1)
{
    *CO1 = (CI1 + CI2) * CI1 + CI3;
}

void CompD(int DI1, int DI2, int *DO1)
{
    *DO1 = (DI1 - DI2) * DI2;
}

long long CompE(int value)
{
    return (value * (long long)value);
}

int AO1, AO2, BO1, CO1;

void SUT(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1, long long *SUTO2)
{
    // identified by pointers values *SUTO1 and *SUTO2 and theirs types
    printf("sut_return_variables_and_initial_values: [{SUTO1:%d},{SUTO2:%I64d}]\n", *SUTO1, *SUTO2);

    // identified by pointers values &AO1 and &AO2 and theirs types
    printf("component_1_return_variables_and_initial_values: [{AO1:%d},{AO2:%d}]\n", AO1, AO2);
    CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);
    // final values &AO1 and &AO2
    printf("component_1_return_variables_and_final_values: [{AO1:%d},{AO2:%d}]\n", AO1, AO2);

    // identified by pointers values &BO1 and its types
    printf("component_2_return_variables_and_final_values: [{BO1:%d}]\n", BO1);
    CompB(SUTI4, SUTI5, SUTI6, &BO1);
    // final value &BO1
    printf("component_2_return_variables_and_final_values: [{BO1:%d}]\n", BO1);

    // need to have DC/CC analysis, because use a variable that have been changed by another component
    printf("component_3_dc_cc_params: [{AO1:%d},{BO1:%d},{SUTI7:%d}]\n", AO1, BO1, SUTI7);
    // identified by pointers values &CO1 and its types
    printf("component_3_return_variables_and_initial_values: [{CO1:%d}]\n", CO1);
    CompC(AO1, BO1, SUTI7, &CO1);
    // final value &CO1
    printf("component_3_return_variables_and_final_values: [{CO1:%d}]\n", CO1);

    // need to have DC/CC analysis, because use a variable that have been changed by another component
    printf("component_4_dc_cc_params: [{CO1:%d}]\n", CO1);
    // identified by pointers values &SUTO2 and its types
    printf("component_4_return_variables_and_initial_values: [{SUTO2:%I64d}]\n", *SUTO2);
    *SUTO2 = CompE(CO1);
    // do not need analysis because not changed/used anymore, output sut, last line already mapped

    // need to have DC/CC analysis, because use a variable that have been changed by another component
    printf("component_5_dc_cc_params: [{CO1:%d},{AO2:%d}]\n", CO1, AO2);
    // identified by pointers values &SUTO2 and its types
    printf("component_5_return_variables_and_initial_values: [{SUTO1:%d}]\n", *SUTO1);
    CompD(CO1, AO2, SUTO1);
    // do not need analysis because not changed/used anymore, output sut, last line already mapped

    // end of sut functions *SUTO1 and *SUTO2
    printf("sut_return_variables_and_final_values: [{SUTO1:%d},{SUTO2:%I64d}", *SUTO1, *SUTO2);
}

int main()
{
    int SUTO1 = 0;
    long long SUTO2 = 0;
    SUT(1, 2, 3, 4, 5, 6, 7, &SUTO1, &SUTO2);
    return 0;
}
