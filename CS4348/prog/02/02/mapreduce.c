#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>

//read a section of the file
int read_words (FILE *f, int start, int end, char* word) {
    int num = 0;
	int read = 0;
	char x[1024];
    // assumes no word exceeds length of 1023
    while (fscanf(f, " %1023s", x) == 1) {
		if(read >= start && read < end){
			if(!strcmp(x, word)){
				num++;
			}
		}
		read++;
    }
	fclose(f);
	return num;
}

//find the total number of words in the file
int count_words (FILE *f) {
	int read = 0;
	char x[1024];
    // assumes no word exceeds length of 1023
    while (fscanf(f, " %1023s", x) == 1) {
		read++;
    }
	return read;
}

int main(int argc, char **argv){
	int num_maps = atoi(argv[1]);
	int BUFSZ = 250;
	int buffer[BUFSZ];
	int child[num_maps];
	int pid = 1;
	int cid = 0;
	int ptc[num_maps][2];
	int ctp[num_maps][2];
	int total = 0;

	//open the file
	FILE *fp;
	fp = fopen(argv[3], "r");

	//find number of words each child needs to read
	int num_words = count_words(fp);
	int to_read = num_words/num_maps;

	//open pipes
	int i;
	for(i=0; i<num_maps; i++){
		pipe(ptc[i]);
		pipe(ctp[i]);
	}

	//fork all new children
	for(i=0; i<num_maps; i++){
		if(pid != 0){
			pid = fork();
			child[i] = pid;
			cid = i;
		}
	}

	//parent process
	if(pid>0){
		for(int i=0;i<num_maps;i++){
			//close unnecessary pipes
			write(ptc[i][0], buffer, sizeof(buffer));
			close(ctp[i][1]);

			//wait for teach child to finish before reading
			int returnstatus;
			waitpid(child[i], &returnstatus, 0);

			//get data from child then close the child
			read(ctp[i][0], &buffer[i], sizeof(int));
			close(ctp[i][0]);
		}
		//add up the total
		for(int i=0; i<num_maps; i++){
			total += buffer[i];
		}
		//print the total
		printf("total: %d\n", total);
	}

	//child process
	if(pid == 0){
		//close unnecessary pipes
    	close(ptc[cid][1]);
    	close(ctp[cid][0]);
		//find section to read
		int start = cid * to_read;
		int end = (cid+1) * to_read;
		//correct for integer division
		if (end >= (num_words-to_read)){
			end = num_words;
		}
		//calc frequency
		fp = fopen(argv[3], "r");
		int frequency = read_words(fp, start, end, argv[2]);
		//print out findings
		printf("child %d started at %d and ended at %d\n", cid, start, end);
		printf("child %d found: %d\n", cid, frequency);
		//send the frequency to parent then close pipe
    	write(ctp[cid][1], &frequency, sizeof(frequency));
    	close(ctp[cid][1]);
	}
}