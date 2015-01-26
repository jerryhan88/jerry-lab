#include <stdio.h>

#define MaxSize 100
int queue[MaxSize];
int head=0,
	tail=0;
int queuein(int);
int queueout(int *);

int main(void)
{
	int c,n;
	printf("]");
	while ((c = getchar()) != EOF){
		if (c =='\n') continue;
		if (c=='i' || c=='I') {
			printf("data--> ");
			scanf("%d", &n);
			if(queuein(n)==-1){
				printf("queue is full\n");
			}
		}
		if (c=='o' || c=='O') {
			if(queueout(&n)==-1)
				printf("queue is empty\n");
			else
				printf("queue data--> %d\n",n);
		}
		printf("]");
	}

	return 0;
}

int queuein(int n)
{
	if((tail+1)%MaxSize != head) {
		queue[tail]=n;
		tail++;
		tail=tail%MaxSize;
		return 0;
	}
	else
		return -1;
}

int queueout(int *n)
{
	if (tail != head) {
		*n=queue[head];
		head++;
		head=head%MaxSize;
		return 0;
	}
	else
		return -1;
}