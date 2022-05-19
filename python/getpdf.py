import fitz


'''
pip install fitz
python -m pip install --upgrade pymupdf
'''

input_file = r'/Users/zxx/Desktop/src.pdf'
doc=fitz.open(input_file)
#select 选择的是一个页数列表
list1 = []
#142页 到 148 就写 141 148
first_num = 132
last_num = 137
for i in range(first_num-1,last_num):
    list1.append(i)
doc.select(list1)
doc2 = fitz.open()
doc2.insert_pdf(doc)
doc2.save(str(first_num)+'-'+str(last_num)+'.pdf')


doc.close()
doc2.close()
