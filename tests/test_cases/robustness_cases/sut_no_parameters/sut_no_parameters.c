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

long CompE(int value)
{
    return value*(long)value;
}

void CompD(int DI1, int DI2, int *DO1)
{
    *DO1 = (DI1 - DI2) * DI2;
}

int AO1, AO2, BO1, CO1;

void SUT()
{
    int a, b;

    CompA(0, 0, 0, &AO1, &AO2);

    CompB(0, 0, 0, &BO1);

    CompC(AO1, BO1, 0, &CO1);

    a = CompE(CO1);

    CompD(CO1, AO2, b);
}