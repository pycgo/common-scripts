package main
// 读取文件 并找出含有字符的行打印出来
import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	file := "/Users/edz/go/src/awesomeProject/test"
	readFile(file)
}

func readFile(filepath string) error {
	f,err := os.Open(filepath)
	defer f.Close()
	if err != nil {
		return err
	}
	buff := bufio.NewReader(f)
	for {
		line, err := buff.ReadString('\n')
		if err == io.EOF {
			break
		}
		if strings.Contains(line,"pass"){
			fmt.Print(line)
		}

	}
	return nil
}
