void CompC(int CI1, int CI2, int CI3, int *CO1)
{
    *CO1 = (CI1 + CI2) * CI1 + CI3;
}

long CompE(int value)
{
    return value*(long)value;
}

void SUT(int *o2, int *o3)
{
    int a, b, c;

    CompC(a, b, c, o3);

    *o2 = CompE(c);
}