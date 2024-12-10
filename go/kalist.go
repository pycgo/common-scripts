package main

import (
	"flag"
	"fmt"
	"github.com/IBM/sarama"
	"log"
	"strings"
)

func main() {
	// 定义命令行参数
	var kafkaAddress = flag.String("kafkaAd", "kafka:9092", "kafka连接地址")
	flag.Parse()

	// 检查命令行参数是否为空
	if *kafkaAddress == "" {
		log.Fatalf("Kafka address cannot be empty")
	}

	// 将逗号分隔的字符串拆分为字符串切片
	brokerList := strings.Split(*kafkaAddress, ",")

	// 创建配置
	config := sarama.NewConfig()
	config.Version = sarama.V3_2_0_0 // 设置Kafka版本，根据你的Kafka集群版本调整

	// 创建新的管理员客户端
	admin, err := sarama.NewClusterAdmin(brokerList, config)
	if err != nil {
		log.Fatalf("Failed to create admin client: %s\n", err)
	}
	defer func() {
		if err := admin.Close(); err != nil {
			log.Fatalf("Failed to close admin client: %s\n", err)
		}
	}()

	// 获取topic列表
	topics, err := admin.ListTopics()
	if err != nil {
		log.Fatalf("Failed to list topics: %s\n", err)
	}

	// 打印topics
	fmt.Println("Available topics:")
	for topic := range topics {
		fmt.Printf("- %s\n", topic)
	}
}
