import fitz


'''
pip install fitz
python -m pip install --upgrade pymupdf
'''

input_file = r'/Users/zxx/Desktop/src.pdf'
doc=fitz.open(input_file)
#select 选择的是一个页数列表
list1 = []
#142页 到 148
for i in range(141,148):
    list1.append(i)

print(list1)
doc.select(list1)
doc2 = fitz.open()
doc2.insert_pdf(doc)
doc2.save('44.pdf')


doc.close()
doc2.close()
