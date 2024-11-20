#include "CompA\CompA.c"
#include "CompB\CompB.h"
#include "CompB\CompX.c"
#include "CompC\CompC.h"
#include "CompD\CompD.h"
#include "CompE\CompE.h"

int AO1, AO2, BO1, CO1;

void sut(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1, long *SUTO2)
{

    CompA(SUTI1, SUTI2, SUTI3, &AO1, &AO2);

    CompB(SUTI4, SUTI5, SUTI6, &BO1);

    CompC(AO1, BO1, SUTI7, &CO1);

    *SUTO2 = CompE(CO1);

    CompD(CO1, AO2, SUTO1);
}