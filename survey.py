import os 
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *       
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk, ImageDraw, ImageOps
import re
import cv2
import numpy as np
import copy

dir_path = os.path.dirname(os.path.realpath(__file__))
global_file_path = ""
window = tk.Tk()
window.title('Shape Reconstruction Application')
window_width = 1125
window_height = 800

label01_outer_boundary_var = tk.StringVar()
label02_alpha_shape_var = tk.StringVar()
label03_x_shape_length_var = tk.StringVar()
label00_NormalisedLength_var = tk.StringVar()

img_user = PhotoImage(file='default2.png')


def readBasicFile(path):
    f = open(path, "r")
    data = []
    for x in f:
        data.append(x)
    return data


# Alpha input format => num_x	num_y
def convertForAlphaShape(data, file_name):
    completeName = os.path.join(dir_path+"/alpha/data2020/", file_name+".txt")         
    file1 = open(completeName, "w")
    FinalText = ""
    for item in data:
        FinalText += item
    file1.write(FinalText)
    file1.close()

# CTShape input format => num_x	num_y
def convertForCTShape(data, file_name):
    completeName = os.path.join(dir_path+"/CT-Shape/Sample_Data/", file_name+".txt")         
    file1 = open(completeName, "w")
    FinalText = ""
    for item in data:
        FinalText += item
    file1.write(FinalText)
    file1.close()

# Simple_Shape input format => num_x,num_y
def convertForSimpleShape(data, file_name):
    file_name = "new_data"
    completeName = os.path.join(dir_path+"/simple_shape/signalprocesser/voronoi/tools/countrydata/", file_name+".txt")         
    file1 = open(completeName, "w")
    FinalText = ""
    for item in data:
        FinalText += item.replace("	", ",")
    file1.write(FinalText)
    file1.close()


# hole_detection_ED input format => num_x	num_y	1
def convertForEmptyDisk(data, file_name):
    completeName = os.path.join(dir_path+"/hole_detection_ED/data/", file_name+".xyz")         
    file1 = open(completeName, "w")
    FinalText = ""
    for item in data:
        FinalText += item.replace("\n", "	1\n")
    file1.write(FinalText)
    file1.close()

# RGG input format => num_x	num_y
def convertForRGG(data, file_name):
    completeName = os.path.join(dir_path+"/RGG/data/", file_name+".txt")         
    file1 = open(completeName, "w")
    FinalText = ""
    for item in data:
        FinalText += item
    file1.write(FinalText)
    file1.close()

# XShape input format => num_x	num_y
def convertForXShape(data, file_name):
    completeName = os.path.join(dir_path+"/X-Shape/input/", file_name+".txt")         
    file1 = open(completeName, "w")
    FinalText = ""
    for item in data:
        FinalText += item
    file1.write(FinalText)
    file1.close()

def chi_shape_alg(file_name, l):

    import pandas as pd
    from polygonX import pgx    
    import matplotlib.pylab as plt
    chi_shape_path = os.path.join(dir_path+"/X-Shape/input/", file_name+".txt")
    f = open(chi_shape_path, "r")
    points = []
    for x in f:
        try:
            temp = x.split()
            if(temp != []):
                points.append(list(map(float, temp)))
        except:
            print("bad input, please delete the last empty line in your input!!")
    plt.scatter([x[0] for x in points],[x[1] for x in points],s=1, color ='black')
    edges = pgx.draw(points,l)
    for edge in edges:
        plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]], color='red')
        # plt.title('l = %.2f' % l)
    plt.axis('off')
    print("done")
    plt.savefig(os.path.join(dir_path+"/X-Shape/output/", file_name+".png"))
    plt.cla()
    plt.clf()

def check_parameter(param, is_float):
    if(is_float):
        if(param.replace('.','',1).isdigit()):
            res = re.findall("\d+\.\d+", param)
            if(res != []):
                if(float(res[0]) <= 1 and float(res[0]) >= 0):
                    return True
                else:
                    print("the number shoud be grater than 0 and less than 1")
            else:
                print("please input a float number(0 < num < 1)")
        else:
            print("please input a float number(0 < num < 1)")
        return False
    else:
        if(param.isdigit()):
            return True
        else:
            return False

def check_float_and_int_parameter(param):
    if(param.replace('.','',1).isdigit()):
        res = re.findall("\d+\.\d+", param)
        if(res != []):
            if(float(res[0]) >= 0):
                return True
    if(param.isdigit()):
        if(int(param)>0):
            return True
        else:
            return False
    return False

def run_all_algorithems(file_name):

    os.system("echo 'CT-Shape Result:'")
    os.system("cd CT-Shape\n ./ct_shape Sample_Data/test.txt".replace("test", file_name))


    os.system("echo 'Empty disk Result:'")
    os.system("cd hole_detection_ED\n ./HoleDetection --in test --p param".replace("test", file_name).replace("param", label01_outer_boundary_var.get()))

    os.system("echo 'RGG Result:'")
    os.system("cd RGG\n ./TestShapeHull data/test.txt".replace("test", file_name))

    os.system("echo 'Simple-Shape Result:'")
    os.system("cd simple_shape\n java -classpath . signalprocesser.voronoi.VoronoiTest value".replace("value", label00_NormalisedLength_var.get()))

    os.system("echo 'alpha-shape Result:'")
    os.system("cd alpha\n ./a.out < data2020/test.txt param".replace("test", file_name).replace("param", label02_alpha_shape_var.get()))


    os.system("echo 'X-Shape Result:'")
    chi_shape_alg(file_name, float(label03_x_shape_length_var.get()))

    print("All results Done!!")

def convertAndRun(file_path):
    if(file_path != ""):
        data = readBasicFile(file_path)
        file_name = str(datetime.datetime.now()).replace(" ", "+")

        convertForCTShape(data, file_name)
        convertForAlphaShape(data, file_name)
        convertForEmptyDisk(data, file_name)
        convertForRGG(data, file_name)
        convertForXShape(data, file_name)
        convertForSimpleShape(data, file_name)
        print("data converted for all algorithm")
        run_all_algorithems(file_name)
        return file_name
    else:
        return ""

def getPathFromUser():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a txt File",filetypes=[("Text file","*.txt")])
    if(isinstance(file_path, str)):
        if(len(file_path)>1):
            global global_file_path
            global_file_path = file_path
            label_path.config(text = "File Path: "+file_path)

def convertImageToDot(image_path, scale, min_color, min_object):
    #check if one around pixel is 255
    def baseCheckAround(close, i , j ,height, width):
        if(i+1 < height):
            if(close[ i+1 , j] == 255):
                return True
            if(j+1 < width):
                if(close[ i+1 , j+1] == 255):
                    return True
            if(j-1 > 0):
                if(close[ i+1 , j-1] == 255):
                    return True
        
        if(i-1 > 0 ):
            if(close[ i-1 , j] == 255):
                return True
            if(j+1 < width):
                if(close[ i-1 , j+1] == 255):
                    return True
            if(j-1 > 0):
                if(close[ i-1 , j-1] == 255):
                    return True
        
        if(j+1 < width):
            if(close[ i , j+1] == 255):
                return True
            if(i+1 < height):
                if(close[ i+1 , j+1] == 255):
                    return True
            if(i-1 > 0):
                if(close[ i-1 , j+1] == 255):
                    return True

        if(j-1 > 0 ):
            if(close[ i , j-1] == 255):
                return True
            if(i+1 < height):
                if(close[ i+1 , j-1] == 255):
                    return True
            if(i-1 > 0):
                if(close[ i-1 , j-1] == 255):
                    return True
        return False

    #check if one around pixel is 0
    def allCheckAround(close, i , j ,height, width):
        res = True
        if(i+1 < height):
            if(close[ i+1 , j] == 255):
                res = False
            if(j+1 < width):
                if(close[ i+1 , j+1] == 255):
                    res = False
            if(j-1 > 0):
                if(close[ i+1 , j-1] == 255):
                    res = False
        
        if(i-1 > 0 ):
            if(close[ i-1 , j] == 255):
                res = False
            if(j+1 < width):
                if(close[ i-1 , j+1] == 255):
                    res = False
            if(j-1 > 0):
                if(close[ i-1 , j-1] == 255):
                    res = False
        
        if(j+1 < width):
            if(close[ i , j+1] == 255):
                res = False
            if(i+1 < height):
                if(close[ i+1 , j+1] == 255):
                    res = False
            if(i-1 > 0):
                if(close[ i-1 , j+1] == 255):
                    res = False

        if(j-1 > 0 ):
            if(close[ i , j-1] == 255):
                res = False
            if(i+1 < height):
                if(close[ i+1 , j-1] == 255):
                    res = False
            if(i-1 > 0):
                if(close[ i-1 , j-1] == 255):
                    res = False
        return res

    # Load image, convert to grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    if(h > scale or w > scale):
        if (w>h):
            factor = int(w / scale)
        else:
            factor = int(h / scale)
        h_f = int(h/factor)
        w_f = int(w/factor)
        gray = cv2.resize(gray, (w_f,h_f))
    height, width = gray.shape
    for i in range(height):
        for j in range(width):
            if (gray[i, j] > min_color):
                gray[i , j] = 255
            else:
                gray[i , j] = 0

    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # # Filter using contour area and remove small noise
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < min_object:
            cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

    # Morph close and invert image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    close = 255 - cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    temp_image = close
    # plt.imshow(close,'Greys_r')
    for i in range(height):
        for j in range(width):
            if (close[i, j] == 0):
                if(not baseCheckAround(close, i , j, height, width)):
                    temp_image[i, j] = 255
                else:
                    temp_image[i, j] = 0

    final_image = copy.deepcopy(temp_image) 
    index_list = []
    index_str = ""
    for i in range(height):
        for j in range(width):
            final_image[i,j] = 255
    
    for i in range(height):
        for j in range(width):
            if(height > 200 or width>200):
                if(i%3 == 0 or j%3 ==0):
                    continue
            if (temp_image[i, j] == 255):
                if(allCheckAround(close, i , j, height, width)):
                    final_image[i, j] = 0
                    index_list.append((i*5,j*5))
                    index_str += str(i*5) + " "+ str(j*5) + "\n"
                else:
                    final_image[i, j] = 255


    text_file = open("new_image_dots.txt", "w")
    n = text_file.write(index_str)
    text_file.close()
    cv2.imwrite("new_image_dots.png", final_image)
    # plt.imshow(final_image,'Greys_r')
    # plt.show()

def imageToDotWindow():
    image_to_dot_window = Toplevel(window)
    image_to_dot_window.title("Image to dot")
    image_to_dot_width = 1100
    image_to_dot_height = 700
    image_to_dot_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    image_to_dot_window.configure(background='white')
    global final_image
    final_image = img_user
    global select_image_flag
    select_image_flag = False
    global make_new_point_flag
    make_new_point_flag = False

    def changePictureUser(label, path):
        resized = Image.open(path)
        resized = resized.resize((400, 400),Image.ANTIALIAS)
        image2 =  ImageTk.PhotoImage(resized)
        label.configure(image = image2)
        label.image = image2

    def getImagePathFromUser():
        root = tk.Tk()
        root.withdraw()
        f_types = [('Jpg Files', '*.jpg'), ('Jpeg Files', '*.jpeg'), ('PNG Files', '*.png')]
        file_path = filedialog.askopenfilename(title="Select a image File",filetypes=f_types)
        if(isinstance(file_path, str)):
            if(len(file_path)>1):
                global global_image_path
                global select_image_flag
                select_image_flag = True
                global_image_path = file_path
                label_image_path.config(text = "File Path: "+file_path)
                changePictureUser(label_user_image,file_path)
    

    style_get_image = Style()
    style_get_image.configure('W.TButton', font =('Times', 15, 'bold'),foreground = 'black', background='white' )
    btn = Button(image_to_dot_window, text = 'Browse image file!' ,style = 'W.TButton', width= 16,command = getImagePathFromUser)
    btn.pack()
    btn.place(relx = 0.42, rely = 0.01, anchor ='nw')

    label_image_path= Label(image_to_dot_window, text='File Path: None', font =('Times', 12, 'bold'))
    label_image_path.pack()
    label_image_path.place(relx = 0.42, rely = 0.06, anchor ='nw')

    frame_user_image = Frame(image_to_dot_window, width=400, height=425)
    frame_user_image.pack_propagate(0)    
    frame_user_image.pack()
    frame_user_image.place( relx = 0.1, rely = 0.1, anchor ='nw')

    label_user_image = Label(frame_user_image, image=img_user, text='Your Image', compound='bottom', font =('Times', 12, 'bold'))
    label_user_image.pack()

    frame_res_image = Frame(image_to_dot_window, width=400, height=425)
    frame_res_image.pack_propagate(0)    
    frame_res_image.pack()
    frame_res_image.place( relx = 0.5, rely = 0.1, anchor ='nw')

    label_res_image = Label(frame_res_image, image=img_user, text='Result Image', compound='bottom', font =('Times', 12, 'bold'))
    label_res_image.pack()

    #  slider 1
    current_value_1 = tk.DoubleVar()
    current_value_1.set(100)
    def slider_1_changed(event):
        label_slider_1_value.configure(text=str(int(current_value_1.get())))

    label_slider_1_name = tk.Label(image_to_dot_window, text = 'Point Density:', font=('Times',12, 'bold'))
    label_slider_1_name.place( relx = 0.19, rely = 0.65, anchor ='nw')
    slider_1 = ttk.Scale(image_to_dot_window,from_=100,to=300,orient='horizontal',length = 350,command=slider_1_changed,variable=current_value_1)
    slider_1.place( relx = 0.32222222222, rely = 0.655, anchor ='nw')
    label_slider_1_value = tk.Label(image_to_dot_window, text = '100', font=('Times',12, 'bold'))
    label_slider_1_value.place( relx = 0.65, rely = 0.65, anchor ='nw')

    #  slider 2
    current_value_2 = tk.DoubleVar()
    current_value_2.set(140)
    def slider_2_changed(event):
        label_slider_2_value.configure(text=str(int(current_value_2.get())))

    label_slider_2_name = tk.Label(image_to_dot_window, text = 'Minimum Color:', font=('Times',12, 'bold'))
    label_slider_2_name.place( relx = 0.19, rely = 0.70, anchor ='nw')
    slider_2 = ttk.Scale(image_to_dot_window,from_=10,to=240,orient='horizontal',length = 350,command=slider_2_changed,variable=current_value_2)
    slider_2.place( relx = 0.32222222222, rely = 0.705, anchor ='nw')
    label_slider_2_value = tk.Label(image_to_dot_window, text = '140', font=('Times',12, 'bold'))
    label_slider_2_value.place( relx = 0.65, rely = 0.70, anchor ='nw')

    #  slider 3
    current_value_3 = tk.DoubleVar()
    current_value_3.set(50)
    def slider_3_changed(event):
        label_slider_3_value.configure(text=str(int(current_value_3.get())))

    label_slider_3_name = tk.Label(image_to_dot_window, text = 'Minimum Object:', font=('Times',12, 'bold'))
    label_slider_3_name.place( relx = 0.19, rely = 0.75, anchor ='nw')
    slider_3 = ttk.Scale(image_to_dot_window,from_=10,to=30000,orient='horizontal',length = 350,command=slider_3_changed,variable=current_value_3)
    slider_3.place( relx = 0.32222222222, rely = 0.755, anchor ='nw')
    label_slider_3_value = tk.Label(image_to_dot_window, text = '50', font=('Times',12, 'bold'))
    label_slider_3_value.place( relx = 0.65, rely = 0.75, anchor ='nw')

    def apply_changes_btn():
        if(select_image_flag):
            convertImageToDot(global_image_path, scale=int(current_value_1.get()), min_color=int(current_value_2.get()), min_object=int(current_value_3.get()))
            changePictureUser(label_res_image,"new_image_dots.png")
            global make_new_point_flag
            make_new_point_flag = True

    
    def done_btn():
        if(make_new_point_flag):
            global global_file_path
            global_file_path = "new_image_dots.txt"
            label_path.config(text = "File Path: "+"new_image_dots.txt")
            image_to_dot_window.destroy()


    style_change = Style()
    style_change.configure('W.TButton', font =('Times', 15, 'bold'),foreground = 'black', background='white' )
    btn_change = Button(image_to_dot_window, text = 'Apply Changes' ,style = 'W.TButton', width= 16,command = apply_changes_btn)
    btn_change.pack()
    btn_change.place(relx = 0.32222222222, rely = 0.85, anchor ='nw')
    
    style_done = Style()
    style_done.configure('W.TButton', font =('Times', 15, 'bold'),foreground = 'black', background='white' )
    btn_done = Button(image_to_dot_window, text = 'Done!' ,style = 'W.TButton', width= 16,command = done_btn)
    btn_done.pack()
    btn_done.place(relx = 0.52222222222, rely = 0.85, anchor ='nw')

    

def image_pad(base_image, x, y, pad=5):
    image = Image.new('RGBA', (x, y + pad))
    image.paste(Image.new('RGB', (x, y), base_image))
    return ImageTk.PhotoImage(image)


def changePicture(label, rotate, path):
    
    resized = Image.open(path)
    ImageDraw.floodfill(resized,xy=(0,0),value=(255,255,255),thresh=10)

    bbox = ImageOps.invert(resized.convert('RGB')).getbbox()
    resized = resized.crop(bbox)
    if(rotate):
        resized = resized.rotate(180)
        resized = resized.transpose(method=Image.FLIP_LEFT_RIGHT)
    resized = resized.resize((250, 250),Image.ANTIALIAS)
    image2 =  ImageTk.PhotoImage(resized)
    label.configure(image = image2)
    label.image = image2

def run_algorithms():
    if(global_file_path != ""):
        if( check_parameter(label01_outer_boundary_var.get(), True) and
            check_parameter(label00_NormalisedLength_var.get(), False) and
            check_float_and_int_parameter(label03_x_shape_length_var.get()) and 
            check_float_and_int_parameter(label02_alpha_shape_var.get())):

            file_name = convertAndRun(global_file_path)
            if(file_name != ""):
                changePicture(label03, True, os.path.join(dir_path+"/X-Shape/output/", file_name+".png"))
                changePicture(label11, False,os.path.join(dir_path+"/CT-Shape/", "output.png"))
                changePicture(label01, True,os.path.join(dir_path+"/hole_detection_ED/", "output.png"))
                changePicture(label10, True, os.path.join(dir_path+"/RGG/", "output.png"))
                changePicture(label00, False, os.path.join(dir_path+"/simple_shape/signalprocesser/voronoi/", "output.PNG"))
                changePicture(label02, True, os.path.join(dir_path+"/alpha/", "output.png"))
        else:
            messagebox.showwarning("Bad Input", "For ES-Shape please input a float number(0 < num < 1) like 0.7\nFor Aplha and X-shape please input a float number (0.0< num< INF).")
    else:
        messagebox.showwarning("File path does not exist!!", "Please select a file from Select File Button.")

# basic input format => num_x	num_y
if __name__ == "__main__":

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height/2 -window_height/2)
    position_right = int(screen_width / 2 - window_width/2)
    window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
   
    style = Style()
    style.configure('W.TButton', font =('Times', 15, 'bold'),foreground = 'black', background='white' )
    btn = Button(window, text = 'Browse input file!' ,style = 'W.TButton', width= 16,command = getPathFromUser)
    btn.pack()
    btn.place(relx = 0.32222222222, rely = 0.01, anchor ='nw')
    
    style1 = Style()
    style1.configure('W.TButton', font =('Times', 15, 'bold'),foreground = 'black', background='white' )
    btn = Button(window, text = 'Image to dot' ,style = 'W.TButton', width= 16,command = imageToDotWindow)
    btn.pack()
    btn.place(relx = 0.52222222222, rely = 0.01, anchor ='nw')


    label_path= Label(window, text='File Path: None', font =('Times', 12, 'bold'))
    label_path.pack()
    label_path.place(relx = 0.42, rely = 0.06, anchor ='nw')

    style2 = Style()
    style2.configure('TButton', font =('Times', 15, 'bold'),foreground = 'black', background='white' )
    btn2 = Button(window, text = 'Run Algorithms' ,style = 'TButton',width= 15,command = run_algorithms)
    btn2.pack()
    btn2.place(relx = 0.42, rely = 0.91, anchor ='nw')
    
    
    frame00 = Frame(window, width=250, height=275)
    frame00.pack_propagate(0)    
    frame00.pack()
    frame00.place( relx = 0.022222222, rely = 0.1, anchor ='nw')
    img00 = PhotoImage(file='default.png')
    label00 = Label(frame00, image=img00, text='Simple-Shape', compound='bottom', font =('Times', 12, 'bold'))
    label00.pack()
    frame00_Normalised_Length_label = tk.Label(window, text = 'Normalised Length:', font=('Times',12, 'bold'))
    frame00_Normalised_Length_label.place( relx = 0.0273, rely = 0.45, anchor ='nw')
    frame01_Normalised_Length_entry = tk.Entry(window, textvariable = label00_NormalisedLength_var, font=('Times',11,'normal'), width=13)
    frame01_Normalised_Length_entry.place( relx = 0.154, rely = 0.45, anchor ='nw')

    
    frame01 = Frame(window, width=250, height=275)
    frame01.pack_propagate(0)    
    frame01.pack()
    frame01.place( relx = 0.266666667, rely = 0.1, anchor ='nw')
    img01 = PhotoImage(file='default.png')
    label01 = Label(frame01, image=img01, text='EC-Shape', compound='bottom', font =('Times', 12, 'bold'))
    label01.pack()

    frame01_outer_boundry_label = tk.Label(window, text = 'Outerboudary Param:', font=('Times',12, 'bold'))
    frame01_outer_boundry_label.place( relx = 0.273, rely = 0.45, anchor ='nw')
    frame01_outer_boundry_entry = tk.Entry(window, textvariable = label01_outer_boundary_var, font=('Times',11,'normal'), width=10)
    frame01_outer_boundry_entry.place( relx = 0.414, rely = 0.45, anchor ='nw')

    frame02 = Frame(window, width=250, height=275)
    frame02.pack_propagate(0)    
    frame02.pack()
    frame02.place( relx = 0.5111111111, rely = 0.1, anchor ='nw')
    img02 = PhotoImage(file='default.png')
    label02 = Label(frame02, image=img02, text='Alpha-Shape', compound='bottom', font =('Times', 12, 'bold'))
    label02.pack()

    frame02_alpha_shape_label = tk.Label(window, text = 'Alpha Param:', font=('Times',12, 'bold'))
    frame02_alpha_shape_label.place( relx = 0.543, rely = 0.45, anchor ='nw')
    frame02_alpha_shape_entry = tk.Entry(window, textvariable = label02_alpha_shape_var, font=('Times',11,'normal'), width=10)
    frame02_alpha_shape_entry.place( relx = 0.6354, rely = 0.45, anchor ='nw')


    frame03 = Frame(window, width=250, height=275)
    frame03.pack_propagate(0)    
    frame03.pack()
    frame03.place( relx = 0.755555555, rely = 0.1, anchor ='nw')
    img03 = PhotoImage(file='default.png')
    label03 = Label(frame03, image=img03, text='X-Shape', compound='bottom', font =('Times', 12, 'bold'))
    label03.pack()

    frame03_self_intersection_label = tk.Label(window, text = 'length-Param:', font=('Times',12, 'bold'))
    frame03_self_intersection_label.place( relx = 0.781, rely = 0.45, anchor ='nw')
    frame03_self_intersection_entry = tk.Entry(window, textvariable = label03_x_shape_length_var, font=('Times',11,'normal'), width=10)
    frame03_self_intersection_entry.place( relx = 0.875, rely = 0.45, anchor ='nw')
    
    frame10 = Frame(window, width=250, height=275)
    frame10.pack_propagate(0)    
    frame10.pack()
    frame10.place( relx = 0.266666667, rely = 0.86, anchor ='sw')
    img10 = PhotoImage(file='default.png')
    label10 = Label(frame10, image=img10, text='RGG', compound='bottom', font =('Times', 12, 'bold'))
    label10.pack()


    frame11 = Frame(window, width=250, height=275)
    frame11.pack_propagate(0)    
    frame11.pack()
    frame11.place( relx = 0.5111111111, rely = 0.86, anchor ='sw')
    img11 = PhotoImage(file='default.png')
    label11 = Label(frame11, image=img11, text='CT-Shape', compound='bottom', font =('Times', 12, 'bold'))
    label11.pack()

    window.configure(background='white')
    window.mainloop()

