#include <stdio.h>
#include <unistd.h>

void funcB(int l){
   	usleep(1000*l);
   	printf("l=%d\n", l);
}

int main(){
	for (int i = 0; i < 20; i++){
		printf("i=%d\n", i);
		//if(i>=10)
			funcB(1000);
		//else
		//	funcB(50);
   	}
   	return 0;
}
