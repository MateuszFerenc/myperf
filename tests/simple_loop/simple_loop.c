#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>

void funcB(unsigned long n){
	unsigned long dumb = 0;
	for(unsigned long i = 0; i < n; i++){
		dumb++;
	}
}

int main(){
	for (int i = 0; i < 200; i++){
    	printf("i=%d\n", i);
		funcB(200000000);	// 200M loop cycles should take aprox. 0.05s, assuming CPU clock is about 4Ghz
   	}
   	return 0;
}
