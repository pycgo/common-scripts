srcfile = 'file/crontab1'
comparefile = 'file/crontab2'

def get_js_name_list(file):
    setJs = set()
    with open(file,'r') as f:
        for line in f:
            if "js" in line:
                item = line.split('node')[1].split('/')[2].strip().strip('>').strip()
                setJs.add(item)
    return setJs


# 返回集合差集，返回setx中内容，和sety 有差异的
def compareJs(setx,sety):
    return setx.difference(sety)


setA = get_js_name_list(srcfile)
setB = get_js_name_list(comparefile)

print(compareJs(setB, setA))
