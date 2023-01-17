package main

import (
	"fmt"
	"reflect"
	"strconv"
)

func main() {
	//定义一个string
	var a string = "10101"
	fmt.Println(reflect.TypeOf(a), a)

	// string 转 int 以及err 示例
	inta, err := strconv.Atoi(a)
	if err != nil {
		println(err.Error())
	} else {
		fmt.Println(reflect.TypeOf(inta), inta)
	}

	//int 到string

	str_int := strconv.Itoa(inta)
	fmt.Println(str_int)

	//string 转int64
	int_64, err := strconv.ParseInt(a, 10, 64)
	fmt.Println(reflect.TypeOf(int_64), int_64)

	// int64 ---> string
	str_int64 := strconv.FormatInt(int_64, 10)
	fmt.Println(reflect.TypeOf(str_int64), str_int64)

	// 字符串转 float64

	str_float64, err := strconv.ParseFloat(a, 64)
	fmt.Println(reflect.TypeOf(str_float64), str_float64)
}
