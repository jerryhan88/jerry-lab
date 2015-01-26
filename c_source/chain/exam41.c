#include <stdio.h>
#include <malloc.h>
#include <string.h>

#define TableSize 1000
#define ModSize 1000

int hash(char *);

struct tfield {
	char name[20];
	char tel[20];
	struct tfield *pointer;
} *dat[TableSize];

struct tfield *talloc(void);

int main(void)
{
	int n;
	char key[12];
	struct tfield *p, *q;

	for (n=0;n<TableSize;n++)
		dat[n]=NULL;

	printf("name tel\n");
	while (p=talloc(), scanf("%s %s",p->name, p->tel)!=EOF){
		n=hash(p->name);
		if (dat[n]==NULL){
			dat[n]=p;
			p->pointer=NULL;
		}
		else {
			q=dat[n];
			while (q->pointer!=NULL)
				q=q->pointer;
			q->pointer=p;
			p->pointer=NULL;
		}
	}

	rewind(stdin);
	printf("\n 탐색할 데이터를 입력하시기 바랍니다.\n");
	while (scanf("%s", key) !=EOF) {
		n=hash(key);
		p=dat[n];
		while (p!=NULL){
			if (strcmp(key,p->name)==0)
				printf("%15s%15s\n",p->name,p->tel);
			p=p->pointer;
		}
	}

	return 0;
}

int hash(char *s)
{
	int n;
	n=strlen(s);
	return (s[0]-'A'+(s[n/2-1]-'A')*26+(s[n-2]-'A')*26*26)%ModSize;
}

struct tfield *talloc(void)
{
	return (struct tfield *)malloc(sizeof(struct tfield));
}