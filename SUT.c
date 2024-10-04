//# include "../CompA/CompA.h"
//# include "../CompB/CompB.h"
//# include "../CompC/CompC.h"
//# include "../CompD/CompD.h"

void CompA (int AI1, int AI2, int AI3, int *AO1, int *AO2){
    *AO1 = AI1 + AI2;
    *AO2 = AI1 * AI3;
}

void CompB (int BI1, int BI2, int BI3, int BI4, int *BO1){
    *BO1 = (BI1+BI2)*(BI3+BI4);
}

void CompC (int CI1, int CI2, int *CO1){
    *CO1 = (CI1+CI2)*CI1;
}

void CompD (int DI1, int DI2, int *DO1){
    *DO1 = (DI1-DI2)*DI2;
}

int AO1, AO2, BO1, CO1;

void SUT(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1){
    int x = 1;
    CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);
    CompB(SUTI4, SUTI5, SUTI6, SUTI7, &BO1);
    CompC(AO1, BO1, &CO1);
    CompD(CO1, AO2, SUTO1);    
}