def mail_from(line):
    if line[:4] == 'MAIL':
        length_wp = white_space(line[4:])
        if length_wp == 0:
            return 0
        else:
            if line[4+length_wp:4+length_wp+5] == 'FROM:':
                length_null = null_space(line[4+length_wp+5:])
                length_path = reverse_path(line[4+length_wp+5+length_null:])
                if length_path == 0:
                    return 0
                else:
                    return 1
            else:
                return 0
    else:
        return 0

def rcpt_to(line):
    if line[:4] == 'RCPT':
        length_wp = white_space(line[4:])
        if length_wp == 0:
            return 0
        else:
            if line[4+length_wp:4+length_wp+3] == 'TO:':
                length_null = null_space(line[4+length_wp+3:])
                length_path = reverse_path(line[4+length_wp+3+length_null:])
                if length_path == 0:
                    return 0
                else:
                    return 1
            else:
                return 0
    else:
        return 0

def data_cmd(line):
    if line == 'DATA':
        return 1
    else:
        return 0


def white_space(line):
    length = 0
    for i in range(len(line)):
        if is_sp(line[i]):
            length+=1
        else:
            break
    return length

def null_space(line):
    length = 0
    for i in range(len(line)):
        if is_sp(line[i]):
            length = white_space(line)
        else:
            break
    return length

def reverse_path(line):
    length = 0
    if line[0] == '<':
        length += 1
        length_mail_box = mail_box(line[1:])
        if length_mail_box == 0:
            length = length_mail_box
            return length
        else:
            length += length_mail_box
            if line[length] == '>':
                length += 1
                return length
            else:
                length = 0
                return length

    else:
        length = 0
        return length


def mail_box(line):
    length = 0
    length_local_part = local_part(line)
    if length_local_part != 0:
        length += length_local_part
        if line[length] == '@':
            length += 1
            length_domain = domain(line[length:])
            if length_domain != 0:
                length += length_domain
            else:
                 length = 0
                 return length
        else:
            length = 0
            return length
    else:
        length = 0
        return length
    return length

def local_part(line):
    return is_string(line)

def is_string(line):
    length = 0
    for i in range(len(line)):
        if is_char(line[i]):
            length += 1
        else:
            break
    return length

def is_char(char):
    special = ['<', '>', '(', ')', '[', ']', '\\', '.', ',', ';', ':', '@', '"']
    if char in special or is_sp(char) or char == '\n':
        return False
    else:
        return True


def domain(line):
    length = 0
    length_element = element(line)
    if length_element != 0:
        length += length_element
        if line[length] == '.':
            length += 1
            length_domain = domain(line[length:])
            if length_domain == 0:
                length = 0
                return length
            else:
                length += length_domain
        else:
            return length
    return length


def element(line):
    length  = 0
    if is_letter(line[0]):
        length += name(line)
    return length


def name(line):
    length = 0
    if is_letter(line[0]):
        length+=1
        length+=let_dig_str(line[1:])
    return length

def let_dig_str(line):
    length = 0
    for i in range(len(line)):
        if let_dig(line[i]):
            length += 1
        else:
            break
    return length

def let_dig(char):
    if is_letter(char) or is_digital(char):
        return True
    else:
        return False

def is_letter(char):
    if 64 < ord(char) < 91 or 96 < ord(char) < 123:
        return True
    else:
        return False

def is_digital(char):
    if 47 < ord(char) < 58:
        return True
    else:
        return False

def is_sp(char):
    if char == ' ' or char == '\t' or char == '':
        return True
    else:
        return False


from socket import *
import sys

while True:
    print('From:')
    from_input = input()
    from_input_ = 'MAIL FROM: <' + from_input + '>'
    if mail_from(from_input_) == 1:
        break
    else:
        print('error')

flag = 0
while True:
    print('To:')
    to_input = input()
    to_list = to_input.split(',')
    for to in to_list:
        to = 'RCPT TO: <' + to.strip() + '>'
        if rcpt_to(to) == 1:
            flag = 0
            continue
        else:
            print('error')
            flag = 1
            break
    if flag == 0:
        break

print('Subject:')
subject_input = input()
subject_input_ = 'Subject: ' + subject_input + '\n\n'

flag = 0
text_list = []
while True:
    if flag == 1:
        break
    print('Message: ')
    while True:
        text_input = input()
        if text_input == '.':
            text_input = 'cnm\n'
            text_list.append(text_input)
            flag = 1
            break
        else:
            text_input+='\n'
            text_list.append(text_input)
            


serverName, serverPort = sys.argv[1:]
serverPort = int(serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


recv = clientSocket.recv(1024).decode()
if recv[:3] != '220':
    print('Cannot connect server')
    clientSocket.close()
clientSocket.send('HELO comp431fa21b.cs.unc.edu'.encode())
recv1 = clientSocket.recv(1024).decode()
if recv1[:3] != '250':
    print('handshake fail')
    clientSocket.close()

clientSocket.send(from_input_.encode())
clientSocket.recv(1024).decode()


for too in to_list:
    too = 'RCPT TO: <' + too.strip() + '>'
    clientSocket.send(too.encode())
    clientSocket.recv(1024).decode()

clientSocket.send('DATA'.encode())
clientSocket.recv(1024).decode()

from_output = 'From: <' + from_input + '>'
clientSocket.send(from_output.encode())

to_output = 'To: '
idex = 0
while idex < len(to_list)-1:
    t = to_list[idex].strip()
    t = '<' + t + '>, '
    to_output+=t
    idex+=1
last_t = '<' + to_list[idex].strip() + '>\n'
to_output += last_t
clientSocket.send(to_output.encode())

clientSocket.send(subject_input_.encode())

for text in text_list:
    clientSocket.send(text.encode())
haha = clientSocket.recv(1024).decode()
print(haha)

clientSocket.send('QUIT'.encode())
clientSocket.recv(1024).decode()
clientSocket.close()
exit()