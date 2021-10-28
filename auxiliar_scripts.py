import pdf2image
from PyPDF2 import PdfFileWriter, PdfFileReader
from PIL import Image
import pytesseract
import time
import os
import inspect
IMG_FOLDER = 'C:\\Users\\jacob\\Desktop\\Escritorio\\Proyectos python\\PDF-OCR\\temp_img\\'
#Tesseract para poder utilizar Pytesseract https://github.com/UB-Mannheim/tesseract/wiki
#En mi caso Tesseract está instalado en la ruta: 
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\jacob\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
#En caso de estar instalado en otra ruta añadirla en lugar de la arriba escrita.

#POPPLER LATEST VERSION https://github.com/oschwartz10612/poppler-windows/releases/
PDF_PATH = 'TEST.pdf'
DPI = 400
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'png'
THREAD_COUNT = 4
USERPWD = None
USE_CROPBOX = False
STRICT = False

def pdf_to_pil(file, folder, output_file):
	start_time = time.time()

	pil_images = pdf2image.convert_from_path(file, dpi = DPI, output_folder = folder, output_file = output_file,first_page = FIRST_PAGE,
											last_page = LAST_PAGE, fmt = FORMAT, thread_count = THREAD_COUNT, userpw = USERPWD, 
											use_cropbox = USE_CROPBOX, strict = STRICT, grayscale = True)
	print('Time taken: ' + str(time.time() - start_time))

def delete_pages(array, file):
	#I think this could be done waaay better with regex. Think about it.
	clean_array = []
	pages = PdfFileReader(file, 'rb').getNumPages()

	for num in array:
		if 'x' in num and '+' in num:

			for x in list(range(0, pages)):
				polin = [int(num.split('x')[0]), int(num.split('x')[1].split('+')[1])]

				if x % int(polin[0]) == 0:

					clean_array.append((x + 1) + polin[1])
		if 'x' in num and '+' not in num:
			for x in list(range(1, pages + 1)):
				if x % int(num.split('x')[0]) == 0:
					clean_array.append(x)

		if '-' in num:
			rang = num.split('-')

			if rang[0] != '' and rang[1] != '':	

				for i in range(int(rang[1]) - int(rang[0])):
					clean_array.append(int(rang[0]) + i)
				clean_array.append(int(rang[1]))
			elif rang[1] == '' and rang[0] != '':

				list(range(0, pages))
				clean_array = list(range(1, pages + 1))[int(rang[0]):]

			else:

				clean_array = list(range(0, pages))[:int(rang[1])]
				clean_array.append(int(rang[1]))
		elif str.isdigit(num) == True:
			clean_array.append(int(num))

	return clean_array

def create_pdf(file, array):
	pages_to_keep = []
	pdf = PdfFileReader(file, 'rb')
	output = PdfFileWriter()
	for i in list(range(1,pdf.getNumPages() + 1)):
		if i not in array:
			pages_to_keep.append(i)
			page = pdf.getPage(i - 1)
			output.addPage(page)

	with open('temp.pdf', 'wb') as temp:
		output.write(temp)

def save_images(pil_images):
	index = 1
	for image in pil_images:
		image.save(IMG_FOLDER + 'page_' + str(index) + '.png')
		index += 1

def get_image_w_h(image_path):
	im = Image.open(image_path)
	width, height = im.size

	return width, height

def extract_from_crop(image, *args):
	for arg in args:
		cropped_img = image.crop(arg)
		cropped_img.show()
		img_text = pytesseract.image_to_string(cropped_img, lang = 'spa')

