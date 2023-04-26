/*
文件片段 ,"position":{"file":"mysql-bin.000369","pos":4,"snapshot":true},"databaseName":
*/
package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var srcPath = flag.String("srcPath", "_metadata", "checkpoint源文件路径")
var desPath = flag.String("desPath", "flushEnv.sh", "")

// getBinPos函数用于获取文件中的bin pos。
func getBinPos(filepath string) (string, int64) {
	// 初始化一个字典，用于存储不同mysqlbin对应的最大pos值。
	dictBinPos := make(map[string]int64)

	// 定义正则表达式匹配的规则。
	pattern := regexp.MustCompile(`"file":"([^"]+)","pos":(\d+)`)

	// 读取文件。
	bytes, err := ioutil.ReadFile(filepath)
	if err != nil {
		panic(err)
	}
	lines := strings.Split(string(bytes), "\n")

	// 对每行进行匹配并更新dictBinPos。
	for _, line := range lines {
		matches := pattern.FindAllStringSubmatch(line, -1)
		if len(matches) >= 2 {
			for _, bindata := range matches {
				mysqlBin := bindata[1]
				pos, _ := strconv.ParseInt(bindata[2], 10, 64)
				if _, ok := dictBinPos[mysqlBin]; !ok {
					dictBinPos[mysqlBin] = pos
				} else if dictBinPos[mysqlBin] > pos {
					dictBinPos[mysqlBin] = pos
				}
			}
		}
	}
	fmt.Println(dictBinPos)
	// 找到最大的mysqlbin对应的最大pos值。
	var maxKey string
	var maxPos int64 = -1
	for k, v := range dictBinPos {
		if k > maxKey {
			maxKey = k
			maxPos = v
		}
	}
	return maxKey, maxPos
}

// 刷新环境变量写入文件，用作shell脚本文件声明环境变量，以备调用。
func flushEnvironmentVariables(srcPath, desPath string) {
	mysqlBin, pos := getBinPos(srcPath)
	fmt.Println(mysqlBin, pos)

	//todo 写文件 export xx=xx
	file, err := os.OpenFile(desPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		fmt.Println("文件打开失败", err)
	}
	//及时关闭file句柄
	defer file.Close()
	write := bufio.NewWriter(file)
	write.WriteString("export MYSQL_BIN=" + mysqlBin + "\n")
	write.WriteString("export POS=" + strconv.FormatInt(pos, 10) + "\n")
	write.Flush()
}

func main() {
	flag.Parse()
	flushEnvironmentVariables(*srcPath, *desPath)
}
