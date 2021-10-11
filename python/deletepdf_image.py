import fitz

input_file = '/testfile/111.pdf'


doc=fitz.open(input_file)

for i in range(0,doc.page_count):
    page = doc[i]
    image = page.get_images()
    print(image[0][1])
    bbox = page.get_image_rects(image[0][0])[image[0][1]]  # get bbox
    # bbox = bbox.irect  # enlarge to include integer pixels
    page.add_redact_annot(bbox)  # define redact annot
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)

    page.insert_image(bbox, xref=image[0][0])
doc.save('222.pdf')
doc.close()
