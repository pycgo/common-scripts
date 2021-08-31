#include <stdio.h>

void pyramid( int n );

int main()
{    
    int n;

    scanf("%d", &n);
    pyramid(n);

    return 0;
}

/* 你的代码将被嵌在这里 */

void pyramid( int n ){
    int i;
    int j;
    // 控制行数
    for(i = 1; i<=n; i++){
        // 打印空格
        for(j = 1; j<=n-i; j++){
            printf(" ");
        }
        // 打完空格打数字
        for(j = 1; j<=i; j++){
            printf("%d ",i);
            // printf("\n");  
        }
        // 两个都打完这一行换行
        printf("\n");
         
        
    }
}
