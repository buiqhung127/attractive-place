import json
import select
import socket

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


def send_req_show_one():
    name_place = input('Input the name of the location that you want to inspect : ')
    msg = '2' + name_place
    client.sendto(bytes(msg, encoding='utf-8'), (HOST, PORT))


def send_req_down_one():
    id_attraction = input('Input the name of attraction : ')
    id_image = input('Input the id of the image : ')
    msg = '3' + id_attraction + ';' + id_image
    client.sendto(bytes(msg, encoding='utf-8'), (HOST, PORT))
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
    return final_data # return an array of JSON, then do whatever you want


def handle_event_show_one():
    encoded_event, add = client.recvfrom(BUFFER_SIZE)
    data = encoded_event.decode('utf-8')
    if data == 'Not Found':
        print('The location is not found !')
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


def receive_image(id_log, id_img): # return false or true 
    file_name = '{}.jpg'.format(id_log + id_img)
    file = open('images-client/' + file_name, "wb")
    while True:
        ready = select.select([client], [], [], timeout)
        if ready[0]:
            data, addr = client.recvfrom(2048)
            if (data == b'Not Found'): # not found is less than 2048 
                print('The file does not exist !')
                return False 
            else : 
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


if __name__ == '__main__':
    msg = b'0'
    client.sendto(msg, (HOST, PORT))
    while IS_RUNNING:
        cmd = receive_query_from_key_board()
        process_command_line(cmd)
    client.close()
