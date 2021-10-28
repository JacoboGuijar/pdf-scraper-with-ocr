
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
import os 
import random
from PIL import Image, ImageTk
import pandas as pd
import auxiliar_scripts

LARGE_FONT = ('verdana', 12)
SMALL_FONT = ('verdana', 8)
MAX_IMG_SIZE = 1080
MY_LANG = 'eng'

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                     
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  
        self.canvas.configure(yscrollcommand=self.vsb.set)                          

        self.vsb.pack(side="right", fill="y")                                       
        self.canvas.pack(side="left", fill="both", expand=True)                     
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw", tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                    
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                     

        self.onFrameConfigure(None)                                                 

    def onFrameConfigure(self, event):                                              
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 

    def onCanvasConfigure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)           


class Example(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)
        self.images_array = []
        self.image_num = 0
        self.pattern_count = 0
        self.x = 0
        self.y = 0
        self.rect = None
        self.rect_count = None

        self.button1 = tk.Button(self.scrollFrame.viewPort, text = 'Choose a PDF', command = self.choose_pdf)
        self.button2 = tk.Button(self.scrollFrame.viewPort, text = 'Delete Pages', command = self.process_pdf, state = 'disabled')
        self.button3 = tk.Button(self.scrollFrame.viewPort, text = 'PDF to images', command = self.pdf_to_images, state = 'disabled')
        self.button4 = tk.Button(self.scrollFrame.viewPort, text = 'Extract Information', command = self.change_screen)
        self.button5 = tk.Button(self.scrollFrame.viewPort, text = 'Load images', command = self.load_images, state = 'disabled')
        self.button6 = tk.Button(self.scrollFrame.viewPort, text = 'Undo', command = self.undo_rectangle, state = 'disabled')
        self.button7 = tk.Button(self.scrollFrame.viewPort, text = 'Show image', command = self.next_image, state = 'disabled')
        self.button8 = tk.Button(self.scrollFrame.viewPort, text = 'Extract text', command = self.process_text, state = 'disabled')

        self.button1.grid(row = 1, column = 1, sticky = 'nesw')
        self.button2.grid(row = 2, column = 1, sticky = 'nesw')
        self.button3.grid(row = 3, column = 1, sticky = 'nesw')
        self.button4.grid(row = 4, column = 1, sticky = 'nesw')

        self.scrollFrame.pack(side="top", fill="both", expand=True)
    
    def choose_pdf(self):
        ftype = [('PDF document files', '*.pdf')]

        self.file = filedialog.askopenfile(mode = 'rt', filetypes = ftype)
        self.button2['state'] = 'normal'

    def process_pdf(self):
        self.button1['state'] = 'disabled'
        self.button2['state'] = 'disabled'
        self.button3['state'] = 'disabled'

        self.popup = popupWindow(self)
        self.popup.validation = True
        self.popup.button['state'] = 'normal'
        self.popup.warning_label['text'] = 'If you want to delete individual pages write them separated by semicolons: 1;4;12.\nIf you want to delete pages in a range write the first and last page separated by a hyphen: 3-15.\nIf you want to delete each N pages you can write: 3x to delete one page every three pages.\n Leave the field blank if you do not want to delete any pages.'
        self.master.wait_window(self.popup.top)

        try:
            to_delete = auxiliar_scripts.delete_pages(self.popup.value.split(';'), self.file.name)
        except AttributeError:
            to_delete = auxiliar_scripts.delete_pages([], self.file.name)
        auxiliar_scripts.create_pdf(self.file.name, to_delete)

        self.button1['state'] = 'normal'
        self.button2['state'] = 'normal'
        self.button3['state'] = 'normal'

    def pdf_to_images(self):
        self.button1['state'] = 'disabled'
        self.button2['state'] = 'disabled'
        self.button3['state'] = 'disabled'
        self.button4['state'] = 'disabled'

        self.popup = popupWindow(self)
        self.popup.validation = True
        self.popup.label['text'] = 'Folder name'
        self.popup.warning_label['text'] = 'Write the name of the folder where each pdf page will be saved as an image file.\nPlease make sure there are no folders with that name.'
        self.master.wait_window(self.popup.top)

        progress_bar = ttk.Progressbar(self.scrollFrame.viewPort, orient = 'horizontal', mode = 'indeterminate')
        progress_bar.grid(row = 5, column = 1, sticky = 'nesw')
        progress_bar.start()
        try:
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '\\' + self.popup.value, exist_ok = True)
            folder = os.path.dirname(os.path.abspath(__file__)) + '\\' + self.popup.value
            print(self.file.name.split('/')[-1].split('.')[0])
            auxiliar_scripts.pdf_to_pil('temp.pdf', folder, self.file.name.split('/')[-1].split('.')[0])
        except TypeError:
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '\\' + 'temporal_directory', exist_ok = True)
            folder = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'temporal_directory'
            print(self.file.name.split('/')[-1].split('.')[0])
            auxiliar_scripts.pdf_to_pil('temp.pdf', folder, self.file.name.split('/')[-1].split('.')[0])
        progress_bar.grid_remove()

        self.button1['state'] = 'normal'
        self.button2['state'] = 'normal'
        self.button3['state'] = 'normal'
        self.button4['state'] = 'normal'

    def change_screen(self):
        self.button1['state'] = 'disabled'
        self.button2['state'] = 'disabled'
        self.button3['state'] = 'disabled'
        self.button4['state'] = 'disabled'
        self.button5['state'] = 'normal'

        self.button1.grid_remove()
        self.button2.grid_remove()
        self.button3.grid_remove()
        self.button4.grid_remove()

        self.button5.grid(row = 0, column = 0, sticky = 'ne')
        self.button6.grid(row = 0, column = 1, sticky = 'ne')
        self.button7.grid(row = 0, column = 2, sticky = 'ne')
        self.button8.grid(row = 0, column = 3, sticky = 'ne')

    def load_images(self):
        self.button5['state'] = 'disabled'

        self.directory = filedialog.askdirectory()

        self.popup = popupWindow(self)
        self.popup.label['text'] = 'How often does the pdf repeat?'
        self.popup.warning_label['text'] = 'If your pdf repeats every 3 pages write: \'3\'. If your PDF follows a pattern where every page is the same write: \'1\'.'
        self.popup.optMenu.grid()
        self.popup.warning_label_2.grid()
        self.master.wait_window(self.popup.top)

        self.load = [] #In case we change directory the images shown won't mix
        sample_images = os.listdir(self.directory)
        sample_images.sort()

        try:
            self.pattern = int(self.popup.value)
            if self.pattern < 0:
                self.pattern = 1
        except Exception:
            self.pattern = 1

        if self.popup.random_state == 'Randomized':
            try:
                if self.pattern < len(sample_images):
                    debug_array = []
                    sample_img_index = random.sample(list(range(int(len(sample_images)/self.pattern))), 3)
                    print(sample_img_index)
                    for img_index in sample_img_index:
                        for index in range(self.pattern):
                            sample_images.append(sample_images[img_index*self.pattern + index])
                            debug_array.append(img_index*self.pattern + index + 1)
                    
                    sample_images = sample_images[-self.pattern*3:]

            except ValueError:
                sample_images = sample_images[random.sample(sample_images, self.value * 3)]
        else:
            try:
                if self.pattern < len(sample_images):
                    sample_images = sample_images[0:self.pattern * 3]
            except ValueError:
                sample_images = sample_images[0:6]

        for image in sample_images:
            img = Image.open(self.directory + '\\' + image)
            #resize images
            if img.height > MAX_IMG_SIZE or img.width > MAX_IMG_SIZE:
                if img.height > img.width:
                    factor = MAX_IMG_SIZE / img.height
                else:
                    factor = MAX_IMG_SIZE / img.width
            resized_img = img.resize((int(img.width * factor), int(img.height * factor)))
            img_dict = {'img': resized_img, 'factor': factor}
            self.images_array.append(img_dict)

        print(sample_images)
        self.load = self.images_array[self.image_num]['img']
        self.render = ImageTk.PhotoImage(self.load)
        self.scrollFrame.canvas['width'] = self.render.width()
        self.scrollFrame.canvas['height'] = self.render.height()
        self.scrollFrame.scrollregion = (0,0,self.images_array[self.image_num]['img'].width, self.images_array[self.image_num]['img'].height)
        self.image_on_canvas = self.scrollFrame.canvas.create_image(0,0,anchor = 'nw', image = self.render)

        self.rect_count = [([]) for i in range(self.pattern)]
        self.array_crop_coords = [([]) for i in range(self.pattern)]
        self.array_crop_coords_dict = [([]) for i in range(self.pattern)]

        self.button5['state'] = 'normal'
        self.button6['state'] = 'normal'
        self.button7['state'] = 'normal'
        self.button8['state'] = 'normal'

        self.mouse_position_label = tk.Label(self.scrollFrame.viewPort, text = 'x: y:')

        self.scrollFrame.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.scrollFrame.canvas.bind('<B1-Motion>', self.on_move_press)
        self.scrollFrame.canvas.bind('<Motion>', self.on_move)
        self.scrollFrame.canvas.bind('<ButtonRelease-1>', self.on_button_release)

    def process_text(self):

        self.button5['state'] = 'disabled'
        self.button6['state'] = 'disabled'
        self.button7['state'] = 'disabled'
        self.button8['state'] = 'disabled'

        list_of_lists = []
        keys = ['image']
        for i in range(len(self.array_crop_coords)):
            for j in range(len(self.array_crop_coords[i])):
                list_of_lists.append([])
                keys.append(self.array_crop_coords_dict[i][j]['name'])
        images_to_process = os.listdir(self.directory)
        images_to_process.sort()
        print(images_to_process)
        progress_window = tk.Toplevel()
        tk.Label(progress_window, text = 'Please wait while the text is extracted')

        progress = 0
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable = progress_var, maximum = 100)
        progress_bar.grid()
        progress_window.pack_slaves()
        progress_step = float(100 / len(images_to_process))

        lst = []
        for k in range(len(images_to_process)):
            progress_window.update()
            img = Image.open(self.directory + '\\' + images_to_process[k])
            i = k % self.pattern
            if i == 0:
                lst = []
                lst.append(images_to_process[k])
            if len(self.array_crop_coords[i]) > 0:

                for j in range(len(self.array_crop_coords[i])):
                    
                    #This is to make sure the rectangles can be created with any starting point
                    if self.array_crop_coords[i][j][0] > self.array_crop_coords[i][j][2] and self.array_crop_coords[i][j][1] > self.array_crop_coords[i][j][3]:
                        self.array_crop_coords[i][j] = (self.array_crop_coords[i][j][2],self.array_crop_coords[i][j][3], self.array_crop_coords[i][j][0], self.array_crop_coords[i][j][1])
                    
                    elif self.array_crop_coords[i][j][0] < self.array_crop_coords[i][j][2] and self.array_crop_coords[i][j][1] > self.array_crop_coords[i][j][3]:
                        self.array_crop_coords[i][j] = (self.array_crop_coords[i][j][0],self.array_crop_coords[i][j][3], self.array_crop_coords[i][j][2], self.array_crop_coords[i][j][1])
                    
                    elif self.array_crop_coords[i][j][0] > self.array_crop_coords[i][j][2] and self.array_crop_coords[i][j][1] < self.array_crop_coords[i][j][3]:
                        self.array_crop_coords[i][j] = (self.array_crop_coords[i][j][2],self.array_crop_coords[i][j][1], self.array_crop_coords[i][j][0], self.array_crop_coords[i][j][3])
                    cropped_image = img.crop(self.array_crop_coords[i][j])
                    #cropped_image.show()
                    if self.array_crop_coords_dict[i][j]['name'].endswith('_email'):
                        texto = auxiliar_scripts.pytesseract.image_to_string(cropped_image, lang = 'eng', config = '--psm 7')
                    else:
                        texto = auxiliar_scripts.pytesseract.image_to_string(cropped_image, lang = MY_LANG, config = '--psm 7')

                    clean_text = texto.strip('\n\x0c')

                    lst.append(clean_text)

            list_of_lists.append(lst)
            img.close()
            progress += progress_step
            progress_var.set(progress)


        #Aquí vamos a crear un metodo que escriba mejor el excel.
        #Por ahora parece que funciona.
        dict_array = []
        for count, lst in enumerate(list_of_lists):
            if self.pattern != 1 and count%self.pattern==1 and len(lst) > 0:
                dic = dict(zip(keys, lst))
                dict_array.append(dic)
            elif self.pattern == 1 and len(lst) > 0:
                dic = dict(zip(keys, lst))
                dict_array.append(dic)
        print(dict_array)
        
        df = pd.DataFrame(data = dict_array, columns = keys)
        df.to_excel('test_2.xlsx')
        progress_window.destroy()

        self.button5['state'] = 'normal'
        self.button6['state'] = 'normal'
        self.button7['state'] = 'normal'
        self.button8['state'] = 'normal'

    def next_image(self):
        self.image_num += 1
        self.pattern_count += 1
        if self.image_num == len(self.images_array):
            self.image_num = 0
        if self.pattern_count == self.pattern:
            self.pattern_count = 0 

        for i in range(self.pattern):
            for j in self.rect_count[i]:
                print('i: {} j: {}'.format(i, j))
                if i == self.pattern_count:
                    self.scrollFrame.canvas.itemconfigure(j, state = 'normal')
                else:
                    self.scrollFrame.canvas.itemconfigure(j, state = 'hidden')

        load = self.images_array[self.image_num]['img']
        render = ImageTk.PhotoImage(load)
        self.scrollFrame.canvas.itemconfig(self.image_on_canvas, image = render)
        self.scrollFrame.canvas.image = render
        self.scrollFrame.canvas.place()
    def on_button_press(self, event):
        if self.scrollFrame.vsb.get()[0] == 0:
            self.start_x = event.x 
            self.start_y = event.y
        else:
            self.start_x = event.x 
            self.start_y = event.y + self.scrollFrame.vsb.get()[0] * self.images_array[self.image_num]['img'].height

        self.rect = self.scrollFrame.canvas.create_rectangle(self.x, self.y, 1,1, outline = 'red', tags = str(self.rect_count))
        self.rect_count[self.pattern_count].append(self.rect)
    def on_move_press(self, event):
        if event.y >= event.y + self.scrollFrame.vsb.get()[0] * self.images_array[self.image_num]['img'].height:
            curX = event.x
            curY = event.y
        else:
            curX = event.x 
            curY = event.y + self.scrollFrame.vsb.get()[0] * self.images_array[self.image_num]['img'].height

        text = 'x: {x} y: {y}\nx: {x} y: {y_test}'.format(x = event.x, y = event.y, y_test = event.y)

        self.scrollFrame.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
        self.mouse_position_label.config(text = text)
    def on_move(self, event):
        text = 'x: {x} y: {y}\nx: {x} y: {y_test}'.format(x = event.x, y = event.y, y_test = event.y)
        self.mouse_position_label.config(text = text)
        #self.mouse_position_label.grid(column = 4, row = 0)
    def on_button_release(self, event):
        end_x = event.x 
        end_y = event.y 
        if event.y >= event.y + self.scrollFrame.vsb.get()[0] * self.images_array[self.image_num]['img'].height:
            end_x = event.x
            end_y = event.y
        else:
            end_x = event.x 
            end_y = event.y + self.scrollFrame.vsb.get()[0] * self.images_array[self.image_num]['img'].height
        start_x_factor = int(self.start_x / self.images_array[self.image_num]['factor'])
        start_y_factor = int(self.start_y / self.images_array[self.image_num]['factor'])
        end_x_factor = int(end_x / self.images_array[self.image_num]['factor'])
        end_y_factor = int(end_y / self.images_array[self.image_num]['factor'])
        coords = 'x1: {start_x} y1: {start_y} x2: {end_x} y2: {end_y}'.format(start_x = self.start_x, start_y = self.start_y, end_x = end_x, end_y = end_y)
        coords_factor = 'x1: {start_x} y1: {start_y} x2: {end_x} y2: {end_y}'.format(start_x = start_x_factor, start_y = start_y_factor, end_x = end_x_factor, end_y = end_y_factor)
        crop_coords = (int(self.start_x / self.images_array[self.image_num]['factor']), 
                       int(self.start_y / self.images_array[self.image_num]['factor']),
                       int(end_x / self.images_array[self.image_num]['factor']), 
                       int(end_y / self.images_array[self.image_num]['factor']))


        self.array_crop_coords[self.pattern_count].append(crop_coords)
        self.popup = popupWindow(self)
        self.popup.validation = True
        self.master.wait_window(self.popup.top)
        self.array_crop_coords_dict[self.pattern_count].append({'name': self.popup.value, 'coords': self.array_crop_coords[self.pattern_count][-1]})
        print(self.array_crop_coords_dict)        
    def undo_rectangle(self):
        if len(self.rect_count[self.pattern_count]) > 0:
            self.rect = self.rect_count[self.pattern_count].pop()
            self.scrollFrame.canvas.delete(self.rect)
            self.array_crop_coords[self.pattern_count].pop()
            self.array_crop_coords_dict[self.pattern_count].pop()
        else:
            print('There are no more areas to delete.')
            self.button8['state'] = 'disabled'

class popupWindow(object):
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        self.value = tk.StringVar()
        self.random_state = tk.StringVar()
        self.validation = False
        self.label = tk.Label(top, text = 'Introduzca un nombre para la seleccion')
        self.label.grid()
        self.entry = tk.Entry(top, textvariable=self.value)
        self.entry.grid()
        self.button = tk.Button(top, text = 'Ok', command = self.cleanup, state = 'disabled')
        self.button.grid()
        self.warning_label = tk.Label(top, text = 'Por favor introduzca un nombre valido.\nSin espacios.\nSin repetir.\nDe más de un caracter.')
        self.warning_label.grid()
        self.optMenu = ttk.Combobox(top,values = ['Not randomized', 'Randomized'], state = "readonly", textvariable=self.random_state)
        #self.optMenu.grid()
        self.warning_label_2 = tk.Label(top, text = 'To randomize the preview images might be helpful to detect small differences in your selection boxes that you might otherwise miss.\n Random sets of images will be chosen but each set will appear in order.\n A set is a succesion of images that belong to one repetition of the PDF.')
        #self.warning_label_2.grid()

        self.value.trace('w', self.validate)
        self.random_state.trace('w', self.validate)

    def validate(self, *args):
        if self.value.get() and self.random_state.get():
            self.button.config(state = 'normal')
            print(self.optMenu.get())

        elif self.validation == True:
            self.button.config(state = 'normal')
        else:
            self.button.config(state = 'disabled')
    def cleanup(self):
        self.random_state = self.optMenu.get()
        self.value = self.entry.get()
        self.top.destroy()

if __name__ == "__main__":
    root=tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()