# include "../CompA/CompA.h"
# include "../CompB/CompB.h"
# include "../CompC/CompC.h"
# include "../CompD/CompD.h"

int W, X, Y, Z;
int retA;

void SUT(int SUTI1, int SUTI2, int SUTI3, int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *SUTO1){
    retA = CompA(SUTI1, SUTI2, SUTI3, &W, &X);
    if (retA != 0)
    {
        return;
    }
    CompB(SUTI4, SUTI5, SUTI6, SUTI7, &Y);
    CompC(W, Y, &Z);
    CompD(Z, X, SUTO1);    
}