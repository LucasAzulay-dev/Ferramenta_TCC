/* This source code is intended to exercise the DC/CC tool developed by Embraer PES3 */
/* Author: jdavison */
/* Revision 0.3 (Nov 04, 2024)*/

#include <stdio.h>
#include "sut.h"

/* ---------------- Software components: f1, f2, f3... ------------*/
int f1(int i1, float i2){
    int a = i1 + (int)i2;
    return a;
}

void f2(float i2, int i3, float *b){
    *b = i3 * i2;
}

void f3(int a, float b, int *o1){
    *o1 = a - (int)b;
}

int f4(int a, float b){
    int o2 = (int)b * 2;
    return o2;
}

/* ---------------------------- The SUT! ----------------------------*/
void sut(int i1, float i2, int i3, int *o1, int *o2){
    int a; 
    float b;

    a = f1(i1, i2);
    f2(i2, i3, &b);
    f3(a, b, o1);
    *o2 = f4(a, b);
}
/* ---------------------------- end SUT ----------------------------*/

