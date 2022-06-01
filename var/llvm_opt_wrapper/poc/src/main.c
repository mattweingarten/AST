#include <stdio.h>
#include "test.h"

int main() {
  printf("hello world\n");
  int a = foo();
  a = a + 10;

  int b = 0;
  for(int i = 0; i < 10; i ++) {
    b = i;
  }

  printf("%d\n", a + b);
  return 0;
}
