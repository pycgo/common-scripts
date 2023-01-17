/*
  读取命令行参数 并写入文件
  下面列举了一些常用的 flag 文件处理参数：
O_RDONLY：只读模式打开文件；
O_WRONLY：只写模式打开文件；
O_RDWR：读写模式打开文件；
O_APPEND：写操作时将数据附加到文件尾部（追加）；
O_CREATE：如果不存在将创建一个新文件；
O_EXCL：和 O_CREATE 配合使用，文件必须不存在，否则返回一个错误；
O_SYNC：当进行一系列写操作时，每次都要等待上次的 I/O 操作完成再进行；
O_TRUNC：如果可能，在打开时清空文件。

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
