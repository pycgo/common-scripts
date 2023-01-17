/*
  读取命令行参数 并写入文件
*/
package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	argsWriteFile(os.Args[1:])
}

func argsWriteFile(args []string) {
	file, err := os.OpenFile("bbb.txt", os.O_WRONLY|os.O_CREATE, 0666)
	if err != nil {
		fmt.Println("文件打开失败", err)
	}
	//及时关闭file句柄
	defer file.Close()
	write := bufio.NewWriter(file)
	for _, value := range args {
		write.WriteString(value + "\n")
	}
	write.Flush()
}
