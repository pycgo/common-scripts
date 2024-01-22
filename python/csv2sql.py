list1 = []
count = 0
with open('test.csv','r') as f:
    for line in f:
        list1 = line.strip().split(',')[1:]
        list1[4] = int(list1[4])
        list1[5] = int(list1[5])

        data = str(list1).replace('[','(').replace(']',')')
        str_start = 'INSERT INTO `xxx` (`table_name`, `table_desc`, `field_name`, `field_desc`, `is_display`) VALUES '
        print(str_start + data + ";")
