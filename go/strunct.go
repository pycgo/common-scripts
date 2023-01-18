package main

import "fmt"

//主结构体
type Qimiao struct {
	Name    string
	Age     int
	Sex     bool
	Hobbies []string
	myHome  Home
}

//套的子结构体
type Home struct {
	P string
}

// 主结构体方法 先写结构体在写方法
func (qmfuc *Qimiao) song(songname string) (restr string) {
	return qmfuc.Name + "唱" + songname
}

//子结构体方法

func (homefac *Home) open() {
	fmt.Println("open", homefac.P)
}

func main() {
	qm := Qimiao{
		Name:    "qimiao",
		Age:     18,
		Sex:     true,
		Hobbies: []string{"play", "eat"},
		myHome: Home{
			P: "北京",
		},
	}

	qm.myHome.open()
}
