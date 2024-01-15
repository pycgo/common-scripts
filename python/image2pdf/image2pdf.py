from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def image_to_pdf(image_path, pdf_path):
    # 打开图片
    image = Image.open(image_path)

    # 获取图片尺寸
    width, height = image.size

    # 创建PDF对象，设置页面尺寸为A4
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # 将图片按比例缩放至适合页面，并居中放置
    if width > height:
        c.drawImage(image_path, 0, 0, 800, 600)
    else:
        c.drawImage(image_path, 0, 0, 600, 800)

    # 保存PDF
    c.save()
for i in range(1,49):

    # 调用函数，将图片转为PDF
    image_to_pdf('image/'+str(i)+'.jpg', 'ppddff/pdf/'+str(i)+'.pdf')
