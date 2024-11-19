void CompA(int AI1, int AI2, int AI3, int *SUTO1, int *SUTO2)
{
    *SUTO1 = AI1 + AI2;
    *SUTO2 = AI2;
}

int main(int SUTI1, int SUTI2, int SUTI3, int *SUTO1, long *SUTO2)
{
    CompA(SUTI1, SUTI2, SUTI3, SUTO1, SUTO2);
}