#include <stdio.h>
#include <string.h>
#include "instrumented_SUT.h"
extern char log_buffer[33554432];
int f1(int x, float y)
{
  int z;
  z = ((int) y) + x;
  return z;
}

void f2(float x, float *y, float *z)
{
  *z = 2 * 1;
  if ((*z) > 3)
  {
    *y = *z;
  }
  else
  {
    *y = -1;
  }
}

void f3(float x, int y, float *z, int *w, float *k)
{
  int aux1;
  float aux2;
  aux1 = ((int) x) + y;
  aux2 = x - ((float) y);
  *w = aux1;
  if ((x < 0) && (y == 1000))
  {
    *k = aux2 + (*z);
  }
  else
  {
    *k = 20.1;
  }
}

float f4(int x, float *y)
{
  return (*y) + 0.1;
}

void f5(float *x, int y, float z, float *w, int *k)
{
  if ((*x) < 0)
  {
    *k = y;
    *w = z;
  }
  else
  {
    *k = 1;
    *w = (float) y;
  }
}

int f6(float *x, float *y)
{
  int o1 = 0;
  *y = (*x) - 20;
  if ((*y) > 100)
  {
    o1 = (*y) - 100;
  }
  return o1;
}

float f7(float x, float *y)
{
  float o3;
  float aux;
  aux = x * (*y);
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
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f1\", \"executionOrder\": \"1\", \"not_used\": {},\"in\": {\"i1\": \"%d\",\"i2\": \"%.3f\"},", i1,i2);
  a = f1(i1, i2);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"a\": \"%d\"}},", a);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f2\", \"executionOrder\": \"2\", \"not_used\": {\"i2\": \"%.3f\"},\"in\": {\"h\": \"%.3f\"},", i2,h);
  f2(i2, &b, &h);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"b\": \"%.3f\",\"h\": \"%.3f\"}},", b,h);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f3\", \"executionOrder\": \"3\", \"not_used\": {},\"in\": {\"i2\": \"%.3f\",\"i3\": \"%d\",\"h\": \"%.3f\"},", i2,i3,h);
  f3(i2, i3, &h, &e, &g);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"e\": \"%d\",\"g\": \"%.3f\"}},", e,g);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f4\", \"executionOrder\": \"4\", \"not_used\": {\"a\": \"%d\"},\"in\": {\"b\": \"%.3f\"},", a,b);
  c = f4(a, &b);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"c\": \"%.3f\"}},", c);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f6\", \"executionOrder\": \"5\", \"not_used\": {},\"in\": {\"c\": \"%.3f\",\"d\": \"%.3f\"},", c,d);
  *o1 = f6(&c, &d);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"d\": \"%.3f\",\"o1\": \"%d\"}},", d,*o1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f5\", \"executionOrder\": \"6\", \"not_used\": {},\"in\": {\"b\": \"%.3f\",\"e\": \"%d\",\"d\": \"%.3f\"},", b,e,d);
  f5(&b, e, d, &f, o2);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"f\": \"%.3f\",\"o2\": \"%d\"}},", f,*o2);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f7\", \"executionOrder\": \"7\", \"not_used\": {},\"in\": {\"f\": \"%.3f\",\"g\": \"%.3f\"},", f,g);
  *o3 = f7(f, &g);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"o3\": \"%.3f\"}},", *o3);
}

