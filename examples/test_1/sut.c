int CompA(int SUTI1){
    return SUTI1 + 1;
}

int CompB(int A01){
    return A01 + 1;
}

int  CompC(int B01){
    return B01 + 1 - B01;
}

int CompD(int SUTI2){
    return SUTI2 * 2;
}

int CompE(int CO1, int DO1){
    return CO1 + DO1;
}

void sut(int SUTI1, int SUTI2, int *SUTO1){
    int A01, BO1, CO1, DO1; 
    A01 = CompA (SUTI1);
    BO1 = CompB (A01);
    CO1 = CompC (BO1);
    DO1 = CompD (SUTI2);
    *SUTO1 = CompE(CO1, DO1);
}
