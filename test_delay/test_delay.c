#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>

void funcB(int l){
   	usleep(1000*l);
   	printf("l=%d\n", l);
}

int main(){
	for (int i = 0; i < 200; i++){
    	printf("i=%d\n", i);
		funcB(100);
   	}
   	return 0;
}
