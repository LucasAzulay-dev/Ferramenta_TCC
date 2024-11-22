int CompA(int SUTI1, int *SUTI2, int SUTI3, int *AO2){
    int AO = SUTI1 + (int)*SUTI2;
    *AO2 = SUTI3/2;
    return AO;
}

void CompB(int SUTI4, int SUTI5, int SUTI6, int SUTI7, int *B01){
    *B01 = SUTI4 + SUTI5 - SUTI6 - SUTI7;
}

int  CompC(int AO1, int B01, int *SUTO2){
    *SUTO2 = AO1 - B01;
    int CO = AO1 + B01 ;
    return CO;
}

void CompD(int CO1, int AO2, int *SUTO1){
    *SUTO1 = CO1 - AO2;
}

void sut(int SUTI1, int SUTI2, int SUTI3, int SUTI4,  int SUTI5, int SUTI6, int SUTI7, int *SUTO1, int *SUTO2){
    int A01, CO1, AO2, B01; 
    A01 = CompA (SUTI1 , &SUTI2 , SUTI3 , &AO2) ;
    CompB (SUTI4 , SUTI5 , SUTI6 , SUTI7 , &B01) ;
    CO1 = CompC (A01 , B01 , SUTO2) ;
    CompD (CO1, AO2 , SUTO1) ;
}
