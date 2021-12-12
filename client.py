import json
import select
import socket
from tkinter import *
from types import SimpleNamespace
BUFFER_SIZE = 10000000
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORT = 8080
IS_RUNNING = True
imgcounter = 1
basename = "image%s.jpg"
timeout = 3


def send_req_show_all():
    msg = b'1'
    client.sendto(msg, (HOST, PORT))
def send_req_show_one(name_place):
    msg = '2' + name_place
    client.sendto(bytes(msg, encoding='utf-8'), (HOST, PORT))

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
    file_name = '{}.jpg'.format(id_log + id_img)
    file = open('images-client/' + file_name, "wb")
    while True:
        ready = select.select([client], [], [], timeout)
        if ready[0]:
            data, addr = client.recvfrom(2048)
            if (data == b'Not Found'):  # not found is less than 2048
                print('The file does not exist !')
                return False
            else:
                print('Downloading...')
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
    name_place=search_input.get('1.0','end-1c')
    data_output.delete('1.0', END)
    send_req_show_one(name_place)
    data_array = handle_event_show_one()
    data_output.insert('1.0', "ID: "+str(data_array["id"])+"\n")
    data_output.insert('2.0', "Tên: "+str(data_array["name"])+"\n")
    data_output.insert('3.0', "Miêu tả: "+str(data_array["description"])+"\n")
    data_output.insert('4.0', "Vị trí địa lí (x,y): "+"("+str(data_array["vị trí địa lý"]["x_coor"])+","+str(data_array["vị trí địa lý"]["y_coor"])+")"+"\n")
def GUI():
    global data_output
    global search_input
    # create window
    window = Tk()
    window.title("Direction searching application")
    window.geometry("1200x900")
    window.configure(background='#FFFFFF')
    # searching sidebar
    search_sidebar = Frame(window, width=200, height=900, bg='#400028')
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
    # data output - picture
    pic_output = Text(output_sidebar, width=100, height=20, bg='#FFFFFF')
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
    pic_output.pack(side=TOP, fill=X)
    # to keep the window loop
    window.mainloop()


if __name__ == '__main__':
    msg = b'0'
    data_output = search_input = None
    client.sendto(msg, (HOST, PORT))
    # while IS_RUNNING:
    #     cmd = receive_query_from_key_board()
    #     process_command_line(cmd)
    GUI()
    client.close()
