package main

import (
	"fmt"
	"log"
	"log/syslog"
	"net"
)

func main() {
	// 创建一个 UDP 服务器
	addr, err := net.ResolveUDPAddr("udp", ":514")
	if err != nil {
		log.Fatal(err)
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	// 创建一个 syslog writer
	writer, err := syslog.New(syslog.LOG_INFO, "my-logger")
	if err != nil {
		log.Fatal(err)
	}
	defer writer.Close()

	// 循环接收日志信息
	buf := make([]byte, 1024)
	for {
		n, addr, err := conn.ReadFromUDP(buf)
		if err != nil {
			log.Fatal(err)
		}
		logMessage := string(buf[:n])

		// 记录日志
		err = writer.Info(logMessage)
		if err != nil {
			log.Println(err)
		}
		fmt.Printf("Received log message from %s: %s\n", addr, logMessage)
	}
}
