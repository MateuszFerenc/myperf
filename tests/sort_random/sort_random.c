#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>

void insertionSort(int arr[], int n)
{
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

void funcB(int arr[], int n){
	insertionSort(arr, n);
}

int main(){
	for (int i = 0; i < 200; i++){
		int arr[10000];

		for (int f = 0; f < 10000 ;f++) {
    		arr[f] = (rand() % 1000);
		}
    	int n = sizeof(arr) / sizeof(arr[0]);
    	printf("i=%d\n", i);
		funcB(arr, n);
   	}
   	return 0;
}
