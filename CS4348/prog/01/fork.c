#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

int main(){
    int BUFSZ = 250;
    char buffer[BUFSZ];

    int pfd[2];
    int pid;

    int cow = 10;

    char * const argv[] = {"/bin/ls", NULL};
    char * const envp[] = {NULL};

    //create pipe
    if(pipe(pfd) == -1){
        perror("pipe");
        exit(EXIT_FAILURE);
    }

    //fork a child to display cow
    pid = fork();
    if(pid < 0){
        perror("fork1 didnt work");
    }

    //childs operations
    if(pid == 0){
        printf("child cow: %d\n", cow);
        //pfd[1] works on my machine instead of pdf[0]
        if(write(pfd[1], "hi there", 9) == -1){
            perror("write");
        }
        cow = 1000;
        printf("child cow: %d\n", cow);
    }

    //parents operations
    else{
        printf("parent cow: %d\n", cow);
        //pfd[0] works on my machine instead of pdf[1]
        if(read(pfd[0], buffer, BUFSZ) == -1){
            perror("read");
        }
        printf("parent cow: %d\n", cow);

        //fork a child to list current directory
        pid = fork();
        if(pid < 0){
            perror("fork");
            exit(EXIT_FAILURE);
        }
        //only child displays dir
        if(pid==0){
            printf("current directory: \n");
            execve("/bin/ls", argv, envp);
        }
    }


    return 0;
}