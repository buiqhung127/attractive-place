import socket
import json


BUFFER_SIZE = 10000000 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORT = 8080
IS_RUNNING = True


def sendReqShowAll():
    msg =  b'1' 
    s.sendto(msg,(HOST,PORT))


def sendReqShowOne():
    name_place = input('Input the name of the location that you want to inspect : ')
    msg = '2' + name_place
    s.sendto(bytes(msg, encoding='utf-8'), (HOST, PORT))


def sendReqDownOne():
    id_attraction = input('Input the name of attraction')
    id_image = input('Input the id of the image')
    msg = '3' + id_attraction + ';' + id_image
    s.sendto(bytes(msg, encoding='utf-8'), (HOST, PORT))


def handleEventShowAll():
    encoded_event, add = s.recvfrom(BUFFER_SIZE)  
    data = encoded_event.decode('utf-8')
    data = data.split(';')
    final_data = [] 
    for datum in data[1:] : 
        datum = json.loads(str(datum))
        final_data.append(datum)
    return final_data


def handleEventShowOne():
    encoded_event, add = s.recvfrom(BUFFER_SIZE)
    data = encoded_event.decode('utf-8')  
    if (data == 'Not Found'):
        print('The location is not found !')
    else:
        print('{}'.format(data))

    return data # json.loads(data) # handle the data later, must convert to json

def handleEventDown():
    encoded_event, add = s.recvfrom(BUFFER_SIZE)
    data = encoded_event.decode('utf-8')  
    if (data == 'Not Found'):
        print('The image is not found !')
    else:
        print('{}'.format(data))
    # return json.loads(data)
    return data # in json file, contain the not found string casee

def processCommandLine(cmd=4): 
    global IS_RUNNING
    if (cmd == 1):
        sendReqShowAll()
        handleEventShowAll()
    elif (cmd == 2):
        sendReqShowOne()
        handleEventShowOne()
    elif (cmd == 3):
        sendReqDownOne()
        handleEventDown()
    else: 
        IS_RUNNING = False

        

def receiveQueryFromKeyBoard(): 
    print('Choose one of these request : ')
    print('1. Load all data that server is managing')
    print('2. Load data from a name of specific location')
    print('3. Download an image from server by id')
    print('4. Disconnect')
    cmd = int(input())
    return cmd 


if __name__ == '__main__':
    msg =  b'0' 
    s.sendto(msg,(HOST,PORT))
    while IS_RUNNING:
        cmd = receiveQueryFromKeyBoard() 
        processCommandLine(cmd)



      


