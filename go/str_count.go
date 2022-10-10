//判断字符串字母的个数

package main

import "fmt"

func main() {
	//建立一个空的map key 是 string 值是 int
	map1 := make(map[string]int)
	str1 := "ssffdfdfdgdsdrfddfff"

	//循环读取 index不用 丢入_  c升级ascii码 需要string 转一下
	for _, c := range str1 {
		//if _, ok := map[key]; ok {
		//    // 存在
		//}
		// 
		//if _, ok := map[key]; !ok {
		//    // 不存在
		//}
		if _, ok := map1[string(c)]; ok {
			map1[string(c)] = map1[string(c)] + 1
		} else {
			map1[string(c)] = 1
		}
	}
	fmt.Println("result", map1)
}
