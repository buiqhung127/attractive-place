import socket
import json



MAXIMUM_CONNECTION = 10
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # ipv4, UDP
HOST = socket.gethostname()
PORT = 8080

data_json = [{
    'id' : '1233123',
    'name' : 'Chua Thien Mu',
    'x_coor' : 20,
    'y_coor' : 30,
    'description' : 'noi day la mot danh lam thang canh thuoc thua thien hue',
    'images' : [
        {
            'id_image' : '391283',
            'directory' : '', # relative directory
            'source' : '3891902j312njals312'
        }
    ]
}]


s.bind((HOST, PORT))


def receiveReq():
    encoded_request, addr = s.recvfrom(BUFFER_SIZE)
    request = encoded_request.decode()
    return request, addr

def handleReqConnection(addr):
    print(addr, 'is connecting to server !')

def handleReqShowAll():
    data = json.loads(data_json[0])
    


def handleReq(request, addr):
    if (request == '0'):
        handleReqConnection(addr)
    elif (request == '1'):
        pass
    elif (request == '2'):
        pass
    elif (request == '3'):
        pass
    else:
        pass


if __name__ == '__main__':
    while True:
        request, addr = receiveReq()
        handleReq(request, addr)
        

# s.listen(10)
# con, add = s.accept() 
#     with con : 
#         try :
#             print('Connected by', add)
#             s.sendto(b'You have connected to the server', add) 
#             while True:
#                 data = con.recv(BUFFER_SIZE) # udp
#                 print(data)
#                 if not data : 
#                     break 
#         finally : 
#             s.close() 

            