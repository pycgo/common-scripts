'''
go run updatezk.go -file=/Users/zxx/GolandProjects/awesomeProject2/zkk/test.yaml -zkpath=/zxx -zookeeper=10.100.42.70:30352
'''
package main

import (
	"flag"
	"fmt"
	"github.com/samuel/go-zookeeper/zk"
	"log"
	"os"
	"time"
)

var file = flag.String("file", "rules.txt", "需要替换的文件")
var zkpath = flag.String("zkpath", "/notuse", "需要替换的zk路径")
var zookeeper = flag.String("zookeeper", "zookeeper:2181", "zk连接地址")

func main() {
	flag.Parse()
	// 连接到ZooKeeper服务器
	conn, _, err := zk.Connect([]string{*zookeeper}, time.Second)
	//conn, _, err := zk.Connect([]string{"10.100.42.70:30352"}, time.Second)
	if err != nil {
		log.Fatalf("无法连接到ZooKeeper服务器：%v", err)
	}
	defer conn.Close()

	// 创建一个节点（如果不存在）
	//path := "/linkflow_5_1_2/metadata/linkflow/versions/0/rules"
	path := *zkpath

	// 定义要设置的YAML数据
	// 从本地文件读取YAML数据
	data, err := os.ReadFile(*file)
	if err != nil {
		log.Fatalf("读取YAML文件时发生错误：%v", err)
	}

	// 检查节点是否存在
	exists, _, err := conn.Exists(path)
	if err != nil {
		log.Fatalf("检查节点是否存在时发生错误：%v", err)
	}

	if exists {
		// 更新节点的值
		_, err = conn.Set(path, data, -1)
		if err != nil {
			log.Fatalf("更新节点值时发生错误：%v", err)
		}
		fmt.Println("节点值已更新！")
	} else {
		// 创建节点
		_, err = conn.Create(path, data, 0, zk.WorldACL(zk.PermAll))
		if err != nil {
			log.Fatalf("创建节点时发生错误：%v", err)
		}
		fmt.Println("节点已创建并设置值！")
	}
}

'''

package main

import (
	"flag"
	"fmt"
	"github.com/samuel/go-zookeeper/zk"
	"log"
	"os"
	"time"
)

var file = flag.String("file", "rules.txt", "需要替换的文件")
var zkpath = flag.String("zkpath", "/notuse", "需要替换的zk路径")
var zookeeper = flag.String("zookeeper", "zookeeper:2181", "zk连接地址")

func main() {
	flag.Parse()
	// 连接到ZooKeeper服务器
	conn, _, err := zk.Connect([]string{*zookeeper}, time.Second)
	//conn, _, err := zk.Connect([]string{"10.100.42.70:30352"}, time.Second)
	if err != nil {
		log.Fatalf("无法连接到ZooKeeper服务器：%v", err)
	}
	defer conn.Close()

	// 创建一个节点（如果不存在）
	//path := "/linkflow_5_1_2/metadata/linkflow/versions/0/rules"
	path := *zkpath

	// 定义要设置的YAML数据
	// 从本地文件读取YAML数据
	data, err := os.ReadFile(*file)
	if err != nil {
		log.Fatalf("读取YAML文件时发生错误：%v", err)
	}

	// 检查节点是否存在
	exists, _, err := conn.Exists(path)
	if err != nil {
		log.Fatalf("检查节点是否存在时发生错误：%v", err)
	}

	if exists {
		// 更新节点的值
		_, err = conn.Set(path, data, -1)
		if err != nil {
			log.Fatalf("更新节点值时发生错误：%v", err)
		}
		fmt.Println("节点值已更新！")
	} else {
		// 创建节点
		_, err = conn.Create(path, data, 0, zk.WorldACL(zk.PermAll))
		if err != nil {
			log.Fatalf("创建节点时发生错误：%v", err)
		}
		fmt.Println("节点已创建并设置值！")
	}
}
