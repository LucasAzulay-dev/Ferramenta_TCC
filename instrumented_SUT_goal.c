#include <stdio.h>
#include <string.h>
#include "instrumented_SUT.h"
extern char log_buffer[33554432];
int f1(int i1, float i2);
void f2(float i2, float *b, float *h);
void f3(float i2, int i3, float *h, int *e, float *g);
float f4(int a, float *b);
void f5(float *b, int e, float d, float *f, int *o2);
int f6(float *c, float *d);
float f7(float f, float *g);
void sut(int i1, float i2, int i3, int *o1, int *o2, float *o3);
int f1(int i1, float i2)
{
  int a;
  a = ((int) i2) + i1;
  return a;
}

void f2(float i2, float *b, float *h)
{
  *h = 2 * i2;
  if ((*h) > 3)
  {
    *b = *h;
  }
  else
  {
    *b = -1;
  }
}

void f3(float i2, int i3, float *h, int *e, float *g)
{
  int aux1;
  float aux2;
  aux1 = ((int) i2) + i3;
  aux2 = i2 - ((float) i3);
  *e = aux1;
  if ((i2 < 0) && (i3 == 1000))
  {
    *g = aux2 + (*h);
  }
  else
  {
    *g = 20.1;
  }
}

float f4(int a, float *b)
{
  return (*b) + 0.1;
}

void f5(float *b, int e, float d, float *f, int *o2)
{
  if ((*b) < 0)
  {
    *o2 = e;
    *f = d;
  }
  else
  {
    *o2 = 1;
    *f = (float) e;
  }
}

int f6(float *c, float *d)
{
  int o1 = 0;
  *d = (*c) - 20;
  if ((*d) > 100)
  {
    o1 = (*d) - 100;
  }
  return o1;
}

float f7(float f, float *g)
{
  float o3;
  float aux;
  aux = f * (*g);
  o3 = aux - 50;
  return o3;
}

void sut(int i1, float i2, int i3, int *o1, int *o2, float *o3)
{
  int a;
  int e;
  float b;
  float c;
  float d;
  float f;
  float g;
  float h;
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f1\", \"executionOrder\": \"1\", \"in\": {\"i1\": \"%d\",\"i2\": \"%f\"}, ",i1,i2);
  a = f1(i1, i2);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"a\": \"%d\"}},\n",a);

  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f2\", \"executionOrder\": \"2\", \"in\": {\"i2\": \"%f\",\"h\": \"%f\"},",i2,h);
  f2(i2, &b, &h);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"b\": \"%f\",\"h\": \"%f\"}},\n",b,h);

  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f3\", \"executionOrder\": \"3\", \"in\": {\"i2\": \"%f\",\"i3\": \"%d\", \"h\": \"%f\",},",i2,i3,h);
  f3(i2, i3, &h, &e, &g);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"e\": \"%d\",\"g\": \"%f\"}},\n",e,g);

  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f4\", \"executionOrder\": \"4\", \"in\": {\"b\": \"%f\"}, ",b);
  c = f4(a, &b);
  sprintf(log_buffer + strlen(log_buffer), "{\"c\": \"%f\"}},\n",c);

  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f6\", \"executionOrder\": \"5\", \"in\": {\"c\": \"%f\",\"d\": \"%f\"}, ",c,d);
  *o1 = f6(&c, &d);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"d\": \"%f\",\"o1\": \"%d\"}},\n",d,*o1);

  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f5\", \"executionOrder\": \"6\", \"in\": {\"b\": \"%f\", \"e\": \"%d\",\"d\": \"%f\"}, ",b, e, d);
  f5(&b, e, d, &f, o2);
  sprintf(log_buffer + strlen(log_buffer), " \"out\": {\"f\": \"%f\",\"o2\": \"%d\"}},\n",f,o2);

  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f7\", \"executionOrder\": \"7\", \"in\": {\"f\": \"%f\",\"g\": \"%f\"}, ",f,g);
  *o3 = f7(f, &g);
  sprintf(log_buffer + strlen(log_buffer), " \"out\": {\"o3\": \"%f\"}},\n",*o3);

