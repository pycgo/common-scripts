#include <stdio.h>

/* 两个整数之间所有的和 如输入源-5 8 结果为21 */
int sum(int m, int n);

int main()
{    
    int m, n;

    scanf("%d %d", &m, &n);
    printf("sum = %d\n", sum(m, n));

    return 0;
}

int sum(int m, int n){
    int end = 0;
    for(int i = m;  i<=n; i++){
        end = end + i;
    }
    return end;
}
