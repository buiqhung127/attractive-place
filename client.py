from ctypes import windll
import json
from os import path
import select
import socket
from tkinter import *
from types import SimpleNamespace
from PIL import ImageTk,Image 

BUFFER_SIZE = 10000000
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# socket.gethostname()
# print(HOST)
# PORT = 8080
# HOST = input("Enter the address : ")
# PORT = int(input("Enter the port : "))
IS_RUNNING = True
imgcounter = 1
basename = "image%s.jpg"
timeout = 3

class LoadImage:
    global img
    def __init__(self,window,File):
        frame = Frame(window)
        self.canvas = Canvas(frame,width=900,height=900)
        self.canvas.pack()
        frame.pack()
        self.orig_img = Image.open(File).resize((640,480), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0,0,image=self.img, anchor="nw")

        self.zoomcycle = 0
        self.zimg_id = None

        window.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Motion>",self.crop)

    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.zimg_id: self.canvas.delete(self.zimg_id)
        if (self.zoomcycle) != 0:
            x,y = event.x, event.y
            if self.zoomcycle == 1:
                tmp = self.orig_img.crop((x-45,y-30,x+45,y+30))
            elif self.zoomcycle == 2:
                tmp = self.orig_img.crop((x-30,y-20,x+30,y+20))
            elif self.zoomcycle == 3:
                tmp = self.orig_img.crop((x-15,y-10,x+15,y+10))
            elif self.zoomcycle == 4:
                tmp = self.orig_img.crop((x-6,y-4,x+6,y+4))
            size = 300,200
            self.zimg = ImageTk.PhotoImage(tmp.resize(size))
            self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg)
def openNewWindow():
    global window
    global App
    global file_name
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(window)
    # sets the title of the
    # Toplevel widget
    newWindow.title("New Window")
    # sets the geometry of toplevel
    newWindow.geometry("600x600")
    # A Label widget to show in toplevel
    Label(newWindow,
          text ="Scroll to zoom").pack(side=TOP,fill=X)
    path = './images-client/' + str(file_name)
    LoadImage(newWindow,path)
 
def send_req_show_all():
    msg = b'1'
    global ip_input
    global port_input
    ip=ip_input.get()
    port=int(port_input.get())
    client.sendto(msg, (ip, port))
  
def send_req_show_one(name_place):
    msg = '2' + name_place
    global ip_input
    global port_input
    ip=ip_input.get()
    port=int(port_input.get())
    
    client.sendto(bytes(msg, encoding='utf-8'), (ip, port))

def send_req_down_one(id_attraction,id_image):  
    msg = '3' + id_attraction + ';' + id_image
    global ip_input
    global port_input
    ip=ip_input.get()
    port=int(port_input.get())
    client.sendto(bytes(msg, encoding='utf-8'), (ip, port))
    return id_attraction, id_image

def handle_event_show_all():
    encoded_event, add = client.recvfrom(BUFFER_SIZE)
    data = encoded_event.decode('utf-8')
    data = data.split(';')
    final_data = []
    print(type(data))
    for datum in data[1:]:
        datum = json.loads(datum)
        final_data.append(datum)
    return final_data  # return an array of JSON, then do whatever you want
def handle_event_show_one():
    global data_output
    encoded_event, add = client.recvfrom(BUFFER_SIZE)
    data = encoded_event.decode('utf-8')
    if data == 'Not Found':
        data_output.delete('1.0', END)
        data_output.insert('1.0', 'Not Found')
    return json.loads(data)  # json.loads(data), should ignore the directory


# def handle_event_down():
#     encoded_event, add = client.recvfrom(BUFFER_SIZE)
#     data = encoded_event.decode('utf-8')
#     if data == 'Not Found':
#         print('The image is not found !')
#         return False
#     else:
#         pass
#     return data  # in json file, contain the not found string casee


def receive_image(id_log, id_img):  # return false or true
    global data_output
    file_name = '{}.jpg'.format(id_log + id_img)
    file = open('images-client/' + file_name, "wb")
    while True:
        ready = select.select([client], [], [], timeout)
        if ready[0]:
            data, addr = client.recvfrom(2048)
            if (data == b'Not Found'):  # not found is less than 2048
                data_output.delete('1.0', END)
                data_output.insert('1.0', 'Not Found')
                return False
            else:
                print('Receiving image...')
                file.write(data)
        else:
            print(f"{file_name} Finish!")
            file.close()
            break
    return True


def process_command_line(cmd=4):
    global IS_RUNNING
    if cmd == 1:
        send_req_show_all()
        print(handle_event_show_all())
    elif cmd == 2:
        send_req_show_one()
        print(handle_event_show_one())
    elif cmd == 3:
        id_loc, id_img = send_req_down_one()
        receive_image(id_loc, id_img)
    else:
        IS_RUNNING = False


def receive_query_from_key_board():
    print('Choose one of these request : ')
    print('1. Load all data that server is managing')
    print('2. Load data from a name of specific location')
    print('3. Download an image from server by id')
    print('4. Exit')
    cmd = int(input())
    return cmd


def all_directions():
    global data_output
    global img
    global output_sidebar
    #delete all data in output_sidebar
    output_sidebar.destroy()
    output_sidebar = Frame(window, width=1000, height=900, bg='orange')
    # data label - direction info
    data_label = Label(output_sidebar, text="Data", font=(
        "Helvetica", 20), bg='orange', fg='#FFFFFF')
    # data output - direction info
    data_output = Text(output_sidebar, width=100, height=20, bg='#FFFFFF')
    # data label - picture
    pic_label = Label(output_sidebar, text="Picture", font=(
        "Helvetica", 20), bg='orange', fg='#FFFFFF')
    # place all elements on the window
    output_sidebar.pack(side=RIGHT, fill=Y)
    data_label.pack(side=TOP, fill=X)
    data_output.pack(side=TOP, fill=X)
    pic_label.pack(side=TOP, fill=X)
    #delete old image
    img=None
    data_output.delete('1.0','end-1c')
    send_req_show_all()
    data_array = handle_event_show_all()
    data_array.reverse()
# loop
    for data in data_array:
        data_output.insert('1.0', "ID: "+str(data["id"])+"\n")
        data_output.insert('2.0', "Tên: "+str(data["name"])+"\n")
        data_output.insert('3.0', "Miêu tả: "+str(data["description"])+"\n")
        data_output.insert('4.0', "Vị trí địa lí (x,y): "+"("+str(data["vị trí địa lý"]["x_coor"])+","+str(data["vị trí địa lý"]["y_coor"])+")"+"\n")
    return data_output


def search_one():
    global data_output
    global search_input
    global pic_output
    global img
    global file_name
    global output_sidebar
    global window
    global index
    global data_array
    global panel
    name_place=search_input.get('1.0','end-1c')
    data_output.delete('1.0', END)
    send_req_show_one(name_place)
    data_array = handle_event_show_one()
    data_output.insert('1.0', "ID: "+str(data_array["id"])+"\n")
    data_output.insert('2.0', "Tên: "+str(data_array["name"])+"\n")
    data_output.insert('3.0', "Miêu tả: "+str(data_array["description"])+"\n")
    data_output.insert('4.0', "Vị trí địa lí (x,y): "+"("+str(data_array["vị trí địa lý"]["x_coor"])+","+str(data_array["vị trí địa lý"]["y_coor"])+")"+"\n")
    index=0
    id_log, id_img = send_req_down_one(str(data_array["name"]), str(data_array["images"][index]["id_image"]))
    receive_image(id_log, id_img)
    file_name = '{}.jpg'.format(id_log + id_img)
    print(file_name)
    img = ImageTk.PhotoImage(Image.open('./images-client/' + file_name).resize((640,480), Image.ANTIALIAS))
    panel = Label(output_sidebar, image=img)
    panel.pack(side=TOP, fill=X)
    btn_zoom = Button(output_sidebar,
                text ="Click to open a new window",
                command = openNewWindow)
    btn_zoom.pack(side=TOP, fill=X)
    btn_next = Button(output_sidebar,
                text ="Next",
                command = next_img)
    btn_next.pack(side=TOP, fill=X)
    btn_previous = Button(output_sidebar,
                text ="Previous",
                command = previous_img)
    btn_previous.pack(side=TOP, fill=X)
    return data_output
def next_img():
    global data_output
    global img
    global file_name
    global output_sidebar
    global index
    global data_array
    global panel
    if index<len(data_array["images"])-1:
        index=index+1
        id_log, id_img = send_req_down_one(str(data_array["name"]), str(data_array["images"][index]["id_image"]))
        receive_image(id_log, id_img)
        file_name = '{}.jpg'.format(id_log + id_img)
        img = ImageTk.PhotoImage(Image.open('./images-client/' + file_name).resize((640,480), Image.ANTIALIAS))
        panel.destroy()
        panel = Label(output_sidebar, image=img)
        panel.pack(side=TOP, fill=X)
        return data_output
    else:
        return data_output
def previous_img():
    global data_output
    global img
    global file_name
    global output_sidebar
    global index
    global data_array
    global panel
    if index>0:
        index=index-1
        id_log, id_img = send_req_down_one(str(data_array["name"]), str(data_array["images"][index]["id_image"]))
        receive_image(id_log, id_img)
        file_name = '{}.jpg'.format(id_log + id_img)
        img = ImageTk.PhotoImage(Image.open('./images-client/' + file_name).resize((640,480), Image.ANTIALIAS))
        panel.destroy()
        panel = Label(output_sidebar, image=img)
        panel.pack(side=TOP, fill=X)
        return data_output
    else:
        return data_output
def connect():
    global ip_input
    global port_input
    ip=ip_input.get()
    port=int(port_input.get())
    client.sendto(msg, (ip, port))
def GUI():
    global data_output
    global search_input
    global pic_output
    global img
    global output_sidebar
    global window
    global ip_input
    global port_input
    # create window
    window = Tk()
    window.title("Direction searching application")
    window.geometry("1200x1000")
    window.configure(background='#FFFFFF')
    # searching sidebar
    search_sidebar = Frame(window, width=200, height=900, bg='#400028')
    lbl_ip=Label(search_sidebar,text="IP:")
    lbl_ip.pack(side=LEFT)
    ip_input=Entry(search_sidebar,width=15)
    ip_input.pack(side=LEFT)
    lbl_port=Label(search_sidebar,text="Port:")
    lbl_port.pack(side=LEFT)
    port_input=Entry(search_sidebar,width=15)
    port_input.pack(side=LEFT)
    btn_connect=Button(search_sidebar,text="Connect",command=connect)
    btn_connect.pack(side=LEFT)
    # searching label - all directions
    search_label = Label(search_sidebar, text="All directions", font=(
        "Helvetica", 20), bg='#400028', fg='#FFFFFF')
    # searching button - all directions
    btn_all = Button(search_sidebar, text="All directions", font=("Helvetica", 15), bg='#ffffff',
                     fg='#400028', width=10, height=1, padx=10, pady=10, command=all_directions)
    # searching lable - one direction
    search_text = Label(search_sidebar, text="Input one direction", font=(
        "Helvetica", 20), bg='#400028', fg='#FFFFFF')
    # searching input
    search_input = Text(search_sidebar, width=20, bg='#FFFFFF',height=1)
    # searching button
    btn_one = Button(search_sidebar, text="Search",
                     width=10, bg='#FFFFFF', fg='#400028',command=search_one)
    # output sidebar
    output_sidebar = Frame(window, width=1000, height=900, bg='orange')
    # data label - direction info
    data_label = Label(output_sidebar, text="Data", font=(
        "Helvetica", 20), bg='orange', fg='#FFFFFF')
    # data output - direction info
    data_output = Text(output_sidebar, width=100, height=20, bg='#FFFFFF')
    # data label - picture
    pic_label = Label(output_sidebar, text="Picture", font=(
        "Helvetica", 20), bg='orange', fg='#FFFFFF')
    # place all elements on the window
    search_sidebar.pack(side=LEFT, fill=Y)
    search_label.pack(side=TOP, fill=X)
    btn_all.pack(side=TOP)
    search_text.pack(side=TOP, fill=X)
    search_input.pack(side=TOP)
    btn_one.pack(side=TOP, fill=X)
    output_sidebar.pack(side=RIGHT, fill=Y)
    data_label.pack(side=TOP, fill=X)
    data_output.pack(side=TOP, fill=X)
    pic_label.pack(side=TOP, fill=X)
    
   
    # to keep the window loop
    window.mainloop()


if __name__ == '__main__':
    msg = b'0'
    index=app=window=output_sidebar=data_output = search_input=pic_output=img=file_name=data_array= None
    ip_input=port_input=None
    # while IS_RUNNING:
    #     cmd = receive_query_from_key_board()
    #     process_command_line(cmd)
    GUI()
    client.close()
