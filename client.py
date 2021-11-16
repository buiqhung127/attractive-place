import socket
import json

BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostname()
PORT = 8080
IS_RUNNING = True


def sendReqShowAll():
    msg =  b'1' 
    s.sendto(msg,(HOST,PORT))


def sendReqShowOne():
    name_place = input('Input the name of the location that you want to inspect : ')


def sendReqDownOne():
    id_attraction = input('Input the name of attraction')
    id_image = input('Input the id of the image')


def handleEventShowAll():
    encoded_event, add = s.recvfrom(BUFFER_SIZE)  
    data = encoded_event.decode('utf-8')
    data = data.split(';')
    final_data = [] 
    for datum in data[1:] : 
        # print('|'+str(datum)+'|')
        # print('\n')
        datum = json.loads(str(datum))
        final_data.append(datum)
    return final_data

def processCommandLine(cmd=4): 
    global IS_RUNNING
    if (cmd == 1):
        sendReqShowAll()
        handleEventShowAll()
    elif (cmd == 2):
        sendReqShowOne()
    elif (cmd == 3):
        sendReqDownOne()
    else: 
        IS_RUNNING = False

    if IS_RUNNING : 
        # handleEventFromServer() 
        pass




# def handleEventFromServer(): 
#     """
#     Type 1 : 
#     REQUESTTYPE._.ID._.NAME._.XCOORDINATE._.YCOORDINATE._.DESCRIPTION._.NUM_OF_IMAGES._.IMAGES.....
#     Example : 1._.123123312._.Chua Thien Mu._.312._.139._noi day la mot danh lam._.5._.3j1319kl54iu2......
#     """
#     encoded_event, add = s.recvfrom(BUFFER_SIZE)  
#     head, data = encoded_event.decode('utf-8')
#     print(data[0:10])
#     head = '0'
#     if head == '0' : 
#         pass
#     elif head == '1':
#         pass
#     elif head == '2' : 
#         pass 
#     elif head == '3':
#         pass 
#     else :
#         pass
        

def receiveQueryFromKeyBoard(): 
    print('Choose one of these request : ')
    print('1. Load all data that server is managing')
    print('2. Load data from a specific location')
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



      


