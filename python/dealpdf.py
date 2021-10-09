import fitz



'''
pip install fitz
python -m pip install --upgrade pymupdf

'''
input_file = r'D:\code\pycode\pdf\input\demo.pdf'
doc=fitz.open(input_file)
#select 选择的是一个页数列表
page = doc.select([0,2])
doc.save(r'output\111.pdf')
doc.close()
