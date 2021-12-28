//httpget 网站内容
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

func main() {
	for _, url := range os.Args[1:] {
		if !strings.HasPrefix(url, "https://") {
			url = "https://" + url
		}
		resp, err := http.Get(url)

		if err != nil {
			fmt.Println(os.Stderr, err)
		}
		fmt.Println(resp.StatusCode)
		data, err := ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			fmt.Println(os.Stderr, err)
			os.Exit(1)
		}
		fmt.Println(data)

	}
}
