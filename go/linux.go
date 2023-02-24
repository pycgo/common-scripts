package main

import (
	"fmt"
	"github.com/xuri/excelize/v2"
	"golang.org/x/crypto/ssh"
	"log"
	"os"
)

func sshLinux(privateKeyPath string) string {

	key, err := os.ReadFile(privateKeyPath)
	if err != nil {
		log.Fatalf("unable to read private key: %v", err)
	}

	// Create the Signer for this private key.
	signer, err := ssh.ParsePrivateKey(key)
	if err != nil {
		log.Fatalf("unable to parse private key: %v", err)
	}

	config := &ssh.ClientConfig{
		User: "root",
		Auth: []ssh.AuthMethod{
			// Use the PublicKeys method for remote authentication.
			ssh.PublicKeys(signer),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	// Connect to the remote server and perform the SSH handshake.

	client, err := ssh.Dial("tcp", "172.16.86.128:22", config)

	if err != nil {
		log.Fatalf("unable to connect: %v", err)
	}
	defer client.Close()
	// 建立新会话
	session, err := client.NewSession()
	defer session.Close()
	if err != nil {
		log.Fatalf("new session error: %s", err.Error())
	}

	result, err := session.Output("uptime;free -g")
	if err != nil {
		fmt.Fprintf(os.Stdout, "Failed to run command, Err:%s", err.Error())
		os.Exit(0)
	}
	return string(result)
}

func writeExcle(data string) {
	f := excelize.NewFile()
	defer func() {
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()

	// Create a new sheet.
	//index, err := f.NewSheet("Sheet2")
	//if err != nil {
	//	fmt.Println(err)
	//	return
	//}

	// Set value of a cell.
	f.SetCellValue("Sheet1", "A2", data)
	//f.SetCellValue("Sheet1", "B2", 100)
	// Set active sheet of the workbook.
	//f.SetActiveSheet(index)
	// Save spreadsheet by the given path.
	if err := f.SaveAs("Book1.xlsx"); err != nil {
		fmt.Println(err)
	}
}

func main() {
	privateKey := "/Users/zxx/.ssh/id_rsa"
	writeExcle(sshLinux(privateKey))
}
