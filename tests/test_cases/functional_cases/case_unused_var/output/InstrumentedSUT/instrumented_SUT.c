#include <stdio.h>
#include <string.h>
#include "instrumented_SUT.h"
extern char log_buffer[33554432];
int f1(int i1, float i2)
{
  int a = i1 + ((int) i2);
  return a;
}

void f2(float i2, int i3, float *b)
{
  *b = i3 * i2;
}

void f3(int a, float b, int *o1)
{
  *o1 = a - ((int) b);
}

int f4(int a, float b)
{
  int o2 = ((int) b) * 2;
  return o2;
}

void sut(int i1, float i2, int i3, int *o1, int *o2)
{
  int a;
  float b;
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f1\", \"executionOrder\": \"1\", \"not_used\": {},\"in\": {\"i1\": \"%d\",\"i2\": \"%.3f\"},", i1,i2);
  a = f1(i1, i2);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"a\": \"%d\"}},", a);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f2\", \"executionOrder\": \"2\", \"not_used\": {},\"in\": {\"i2\": \"%.3f\",\"i3\": \"%d\"},", i2,i3);
  f2(i2, i3, &b);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"b\": \"%.3f\"}},", b);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f3\", \"executionOrder\": \"3\", \"not_used\": {},\"in\": {\"a\": \"%d\",\"b\": \"%.3f\"},", a,b);
  f3(a, b, o1);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"o1\": \"%d\"}},", *o1);
  sprintf(log_buffer + strlen(log_buffer), "{\"function\": \"f4\", \"executionOrder\": \"4\", \"not_used\": {\"a\": \"%d\"},\"in\": {\"b\": \"%.3f\"},", a,b);
  *o2 = f4(a, b);
  sprintf(log_buffer + strlen(log_buffer), "\"out\": {\"o2\": \"%d\"}},", *o2);
}

