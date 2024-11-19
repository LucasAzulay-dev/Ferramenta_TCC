/* This source code is intended to exercise the DC/CC tool developed by Embraer PES3 */
/* Author: jdavison */
/* Revision 0.3 (Nov 04, 2024)*/

#include <stdio.h>
#include "sut.h"

/* ---------------- Software components: f1, f2, f3... ------------*/
int f1(int x, float y){
    int z;
    z = (int)y + x;
    return z;
}

void f2(float x, float *y, float *z){
    *z = 2 * x;
    if(*z > 3){
        *y = *z;
    }
    else{
        *y = -1;
    }
}

void f3(float x, int y, float *z,   int *w, float *k){
    int aux1;
    float aux2;
    aux1 = (int)x + y;
    aux2 = x - (float)y;

    *w = aux1;
    if((x < 0) && (y == 1000)){
        *k = aux2 + *z;
    }
    else{
        *k = 20.1;
    }
}

float f4(int x, float *y){
    return *y + 0.1;
}

void f5(float *x, int y, float z,   float *w, int *k){

    if(*x < 0){
        *k = y;
        *w = z;
    }
    else{
        *k = 1;
        *w = (float)y;
    }
}

int f6(float *x, float *y){
    int o1 = 0;
    *y = *x - 20;
    if(*y > 100){
        o1 = *y - 100; 
    }
    return o1;
}

float f7(float x, float *y){
    float o3, aux;
    aux = x * (*y);

    o3 = aux - 50; 
    return o3;
}

/* ---------------------------- The SUT! ----------------------------*/
void sut(int i1, float i2, int i3,   int *o1, int *o2, float *o3){
    int a, e; 
    float b, c, d, f, g, h;

    a = f1(i1, i2);
    f2(i2, &b, &h);
    f3(i2, i3, &h, &e, &g);
    c = f4(a, &b);
    *o1 =f6(&c, &d);
    f5(&b, e, d, &f, o2);
    *o3 = f7(f, &g);
}
/* ---------------------------- end SUT ----------------------------*/

