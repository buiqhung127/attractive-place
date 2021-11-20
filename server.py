import json
import socket
import time

from read_places import get_places

MAXIMUM_CONNECTION = 10
BUFFER_SIZE = 10000000  # 10 mb
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ipv4, UDP
HOST = socket.gethostname()
PORT = 8080

data_json = get_places()
s.bind((HOST, PORT))


def receive_req():
    encoded_request, addr = s.recvfrom(BUFFER_SIZE)
    request = encoded_request.decode()
    return request, addr


def handle_req_connection(addr):
    print(addr, 'is connecting to server !')


def handle_req_show_all(addr):
    data = ''
    for place in data_json['list']['resources']:
        data = data + ';' + json.dumps(place)
    s.sendto(bytes(data, encoding='utf-8'), addr)
    print('Handled the show all request !')


def handle_req_show_one(request, addr):
    request = request[1:]
    flag = False
    for data in data_json['list']['resources']:
        if data['name'] == request:
            s.sendto(bytes(json.dumps(data), encoding='utf-8'), addr)
            flag = True

    if not flag:
        s.sendto(bytes('Not Found', encoding='utf-8'), addr)


def handle_req_down(request, addr):
    request = request[1:]
    request = request.split(';')
    flag = False
    for data in data_json['list']['resources']:
        if data['name'] == request[0]:
            for image in data['images']:
                if image['id_image'] == int(request[1]):
                    # s.sendto(bytes(json.dumps(image), encoding='utf-8'), addr)
                    send_image(image['directory'], addr)
                    flag = True
    if not flag:
        s.sendto(bytes('Not Found', encoding='utf-8'), addr)


def handle_req(request, addr):
    if request[0] == '0':
        handle_req_connection(addr)
    elif request[0] == '1':
        handle_req_show_all(addr)
    elif request[0] == '2':
        handle_req_show_one(request, addr)
    elif request[0] == '3':
        handle_req_down(request, addr)
    else:
        pass


def send_image(directory, addr):
    file = open(directory, 'rb')
    image_data = file.read(2048)

    while image_data:
        s.sendto(image_data, addr)
        image_data = file.read(2048)
        time.sleep(0.02)  # Give receiver a bit time to save


if __name__ == '__main__':
    while True:
        request, addr = receive_req()
        handle_req(request, addr)
