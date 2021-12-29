// go 的 命令行参数 类似Python的argsprase
package main

import (
	"flag"
	"fmt"
	"strings"
)

var n = flag.Bool("n", false, "默认换行")
var s = flag.String("s", " ", "分隔符，默认空格")

func main() {

	flag.Parse()
	fmt.Print(strings.Join(flag.Args(), *s))
	if !*n {
		fmt.Println()
	}
}
