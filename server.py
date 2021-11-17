import socket
import json

from client import handleEventShowAll



MAXIMUM_CONNECTION = 10
BUFFER_SIZE = 10000000 # 10 mb
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ipv4, UDP
HOST = socket.gethostname()
PORT = 8080

data_json = [{
    'id' : '1233123',
    'name' : 'Chua Thien Mu',
    'x_coor' : '20',
    'y_coor' : '30',
    'description' : 'noi day la mot danh lam thang canh thuoc thua thien hue',
    'images' : [
        {
            'id_image' : '391283',
            'directory' : '', # relative directory
            'source' : '3891902j312njals312'
        }
    ]
},
{
    'id' : '48908312',
    'name' : 'Kinh Thanh Hue',
    'x_coor' : '20',
    'y_coor' : '30',
    'description' : 'kkk thanh hue',
    'images' : [
        {
            'id_image' : '911283',
            'directory' : '', # relative directory
            'source' : '091302j312njals312'
        },
        {
            'id_image' : '123283',
            'directory' : '', # relative directory
            'source' : '1902j312njals312'
        }
    ]
}
]


s.bind((HOST, PORT))


def receiveReq():
    encoded_request, addr = s.recvfrom(BUFFER_SIZE)
    request = encoded_request.decode()
    return request, addr

def handleReqConnection(addr):
    print(addr, 'is connecting to server !')


def handleReqShowAll(addr):
    data =''
    for place in data_json:  
        data =  data + ';' + json.dumps(place)
    s.sendto(bytes(data, encoding='utf-8'), addr)
    print('Handled the show all request !')


def handleReqShowOne(request, addr) :
    request = request[1:]
    # print('|{}|'.format(request))
    flag = False
    for data in data_json: 
        if (data['name'] == request):
            s.sendto(bytes(json.dumps(data), encoding='utf-8'), addr)
            flag = True
    
    if not flag:
        s.sendto(bytes('Not Found', encoding='utf-8'), addr)


def handleReqDown(request, addr): 
    request = request[1:]
    request = request.split(';')
    # print('|{}|'.format(request))
    flag = False
    for data in data_json: 
        if data['name'] == request[0]:
            for image in data['images'] : 
                if image['id_image'] == request[1] : 
                    s.sendto(bytes(json.dumps(image), encoding='utf-8'), addr)
                    flag = True
    
    if not flag:
        s.sendto(bytes('Not Found', encoding='utf-8'), addr)


def handleReq(request, addr):
    if (request[0] == '0'):
        handleReqConnection(addr)
    elif (request[0] == '1'):
        handleReqShowAll(addr) 
    elif (request[0] == '2'):
        handleReqShowOne(request, addr) 
    elif (request[0] == '3'):
        handleReqDown(request, addr)
    else:
        pass


if __name__ == '__main__':
    while True:
        request, addr = receiveReq()
        handleReq(request, addr)
        

