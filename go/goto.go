/*
  程序A循环 到5的时候 打断A 并跳转B 去执行
*/
package main

import "fmt"

func main() {
	A:
		for a := 0; a < 10; a++ {
			if a == 5 {
				break A
				goto B
			}
			fmt.Println(a)
	
		}
	B:
		fmt.Println("BBB")
}
