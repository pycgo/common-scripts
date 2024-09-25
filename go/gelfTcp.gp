package main

import (
	"fmt"
	"gopkg.in/Graylog2/go-gelf.v2/gelf"
	"os"
	"runtime"
	"strconv"
	"sync"
	"time"
)

// GelfWriter is a pointer to a gelf.UPDWriter
var GelfWriter *gelf.TCPWriter

// GelfHostname is used across GELF messages to provide the source field
var GelfHostname string

func createLogger() {
	//GelfWriter, _ = gelf.NewUDPWriter("10.100.42.133:12201")
	GelfWriter, _ = gelf.NewTCPWriter("192.168.50.35:12201")
	//GelfWriter, _ = gelf.NewUDPWriter("192.168.50.35:12201")
	//GelfWriter.CompressionType = gelf.CompressNone
	//GelfWriter.CompressionType = gelf.CompressGzip // Set the compression type to Zlib
	//GelfWriter.CompressionLevel = gzip.BestCompression
	//GelfWriter.CompressionType = gelf.CompressZlib // Set the compression type to Zlib
	//GelfWriter.CompressionLevel = zlib.BestCompression
}
func wrapBuildMessage(s string, f string, l int32, ex map[string]interface{}) *gelf.Message {
	/*
		Level is a stanard syslog level
		Facility is deprecated
		Line is deprecated
		File is deprecated
	*/
	m := &gelf.Message{
		Version:  "1.1",
		Host:     GelfHostname,
		Short:    s,
		Full:     f,
		TimeUnix: float64(time.Now().Unix()),
		Level:    l,
		Extra:    ex,
	}
	return m
}
func logMsg(w *sync.WaitGroup) {
	var level int32
	now := time.Now()
	currentTimeStr := now.Format("2006-01-02 15:04:05")
	fullMsg := "《十万个为什么》的名称源于苏联科学文艺作家伊林（真名为伊利亚·雅科甫列维奇·马尔夏克）的作品《十万个为什么》。而伊林又是从诗人吉卜林的诗句：“五千个在哪儿／七千个怎么样／十万个为什么”中，选用“十万个为什么”作书名的。伊林的《十万个为什么》大约有五万多字，书里解答的“为什么”并没有十万个。“十万”（俄语：сто тысяч，“一百个千”）是一个虚指，用来形容许多。第一版只有900多个“为什么”，现在也只有3000多个“为什么”。虽然中国版的《十万个为什么》也没有达到“十万”，但是规模却远远大于伊林的作品，有十余册之多，堪称一部小型百科全书。“为什么”就是《十万个为什么》丛书中的一个个条目（主题）。每一个条目就是一篇几千字的科学普及文学作品。因为丛书中条目的标题通常采用“为什么……？”的表达方式，所以许多时候都用“为什么”来指代一个问题和此问题的解答诠释。版本中译本伊林的《十万个为什么》最早由董纯才译成中文，上海开明书店于1934年出版，[1]是“开明青年丛书”的一部分。因为广受欢迎，《十万个为什么》不断修订，1949年3月印了第10版。[2]1938年，郑缤的《十万个为什么》中译本由中国青年出版社出版。[3]中国大陆地区《十万个为什么》在中国大陆地区有多个不同的版本，其中，以上海的少年儿童出版社出版的较为知名。上海少儿版第一版少年儿童出版社从1958年开始酝酿出版一套大型科普读物。共计约请了200多位作者撰稿。经过半年多时间，选用了100多位作者的稿件，于1960年7月开始出版第1版，分为数学、物理、化学、天文气象、动物、农业、地质矿物、生理卫生8个分册，共收1484个问题，100万字。到1964年4月，三年中重印11次、发行580多万册。青年作家叶永烈写了其中300多条，是写得最多的作家，在此之后他也参与了之后五个版本的写作。第二版1964年开始修订、编辑第2版，亦被称为“修订版”。第2版定为14分册，至1966年2月止出齐。在这次修订编辑中，少年儿童出版社约请了更多的科技工作者和科普作者写作，如茅以升、苏步青、李四光、竺可桢、张钰哲、戴文赛、钱崇澍、傅连璋等。第三版（“工农兵版”）文化大革命中，1971年起，根据当时的思潮，改为工农兵读物由上海人民出版社出版，并增订到二十一册，出版了第3版，即“工农兵版”。前14册封面橘黄色，工农兵高擎《毛泽东选集》图案为封面。后7册蓝色。第18和21册由少年儿童出版社出版。其发行量达到上千万册。该版本有大量政治和经济宣传内容。比如第三册“工业”的封面有“独立自主、自力更生”的毛主席语录；再如“为什么三千吨的船台能造万吨巨轮？”条目中说：“上海船厂的工人、革命干部和技术人员实行‘三结合’……批判了叛徒、内奸、工贼刘少奇‘造船不如买船，买船不如租船’的洋奴哲学、爬行主义”。第四版文革之后，从1980年4月起至1981年10月，出版了第4版仍为14个分册，封面深蓝色。去掉了阶级斗争的内容，但仍有政治干涉学术的内容，譬如认为宇宙有限和大爆炸是唯心主义。这14个分册的版本又称为“改革版”[4]。1990年，在第4版14个分册的基础上又增加了10个分册的“续编本”，1993年3月一次出齐。至此，《十万个为什么》共计24个分册。第五版1999年，《十万个为什么》“新世纪版”出版，该版为第5版。共有12册：数学、物理、化学、动物、植物、人体科学、地球科学、宇宙科学、环境科学、信息科学、工程科学、索引资料。第六版由上海世纪出版股份有限公司主办。第六版从内容到形式都将实现重大突破，如很多问题将不再设计标准答案，并形成从图书到电子产品、网络产品的立体出版格局。第六版共18卷为全彩色图文印刷，以及黑白普及本、网络电子版等于2013年陆续面世。其大部分问题都是从全中国少年儿童中广泛征集而来的。[5]18个分册为：基础卷：数学、物理、化学、天文、地球、生命。专题卷：动物、植物、古生物、医学、建筑与交通、电子与信息。热点卷：大脑与认知、海洋、能源与环境、航空与航天、武器与国防、灾难与防护。据《十万》官方微博消息，第六版于2013年8月13日亮相上海书展，在2013年上海书展首发时便创下了3500套的销量[4]。全书共600万字，7000余幅彩色图片，收录4500个代表科技发展前沿和青少年关心的热点问题，其中有80%是新问题。此外，还设有“科学人”、“微博士”、“实验场”、“微问题”等栏目。目前繁体版本的版权是在\"畅谈国际文化事业股份有限公司\"所出版的“十万个为什么？非知不可”。总共72册。奖项与荣誉上海少年儿童出版社出版的《十万个为什么》先后获得1998年“国家科技进步二等奖”、首届“中国出版政府奖”图书奖（2008年）、“感动共和国的50本书”之一等奖项与荣誉[6]。其他版本目前中国大陆已有多间出版社出版了不同版本的《十万个为什么》，如天津人民出版社、北京教育出版社、北方妇女儿童出版社、华文出版社等。然而，上海少年儿童出版社认为这些出版社出版的《十万个为什么》涉嫌侵权，为此，出版社发起维权行动。2000年1月，国家版权局向相关部门发出《关于立即查缴盗版图书〈十万个为什么〉的紧急通知》，但均未能有效制止盗版《十万个为什么》乱象。少年儿童出版社还将“十万个为什么”作为商标提出注册申请，以寻求对“十万个为什么”获得注册商标专用权方面的保护，但注册申请遭驳回，原因是“‘十万个为什么’已成为科普读物上常用的书名，将其作为商标使用在书籍等商品上，难以起到区别商品来源的作用，缺乏商标的显著性[7]”。"
	shortMsg := "Stack trace here"
	//fullMsg := "Stack trace here"
	level = 3
	_, file, line, _ := runtime.Caller(1)
	customExtras := map[string]interface{}{"file": file, "line": line, "job_name": "/api/wx/authorize?signature=83f966fce29527d99a4a3fc474590ad2b6a316fc&timestamp=1726044316&nonce=1341294038&encrypt_type=aes&msg_signature=25595bc711bee71d8b377266e73981e4213e289c", "time": currentTimeStr}
	customMessage := wrapBuildMessage(shortMsg, fullMsg, level, customExtras)
	//println(customExtras)
	GelfWriter.WriteMessage(customMessage)
	w.Done()
}

func main() {
	fmt.Println("Starting tests")
	GelfHostname, _ = os.Hostname()
	createLogger()
	var wait sync.WaitGroup

	for i := 0; i < 10; i++ {
		//time.Sleep(1 * time.Second)
		wait.Add(1)
		go logMsg(&wait)
		fmt.Println("Starting tests" + strconv.Itoa(i))
	}
	wait.Wait()
}
