def from_who(line):
    length_wp = white_space(line[4:])
    length_null = null_space(line[4 + length_wp + 5:])
    length_path = reverse_path(line[4 + length_wp + 5 + length_null:])
    return line[4 + length_wp + 5 + length_null + 1: 4 + length_wp + 5 + length_null + length_path - 1]

def to_who(line):
    length_wp = white_space(line[4:])
    length_null = null_space(line[4+length_wp+3:])
    length_path = reverse_path(line[4+length_wp+3+length_null:])
    return line[4+length_wp+3+length_null+1: 4+length_wp+3+length_null+length_path-1]


def mail_from(line):
    if line[:4] == 'MAIL':
        length_wp = white_space(line[4:])
        if length_wp == 0:
            error_msg(500)
            return 0
        else:
            if line[4+length_wp:4+length_wp+5] == 'FROM:':
                length_null = null_space(line[4+length_wp+5:])
                length_path = reverse_path(line[4+length_wp+5+length_null:])
                if length_path == 0:
                    return 0
                else:
                    length_nul = null_space(line[4+length_wp+5+length_null+length_path:])
                    if line[4+length_wp+5+length_null+length_path+length_nul] == '\n':
                        correct_msg()
                        return 1
                    else:
                        error_msg(500)
                        return 0
            else:
                error_msg(500)
                return 0
    else:
        error_msg(500)
        return 0

def rcpt_to(line):
    if line[:4] == 'RCPT':
        length_wp = white_space(line[4:])
        if length_wp == 0:
            error_msg(500)
            return 0
        else:
            if line[4+length_wp:4+length_wp+3] == 'TO:':
                length_null = null_space(line[4+length_wp+3:])
                length_path = reverse_path(line[4+length_wp+3+length_null:])
                if length_path == 0:
                    return 0
                else:
                    length_nul = null_space(line[4+length_wp+3+length_null+length_path:])
                    if line[4+length_wp+3+length_null+length_path+length_nul] == '\n':
                        correct_msg()
                        return 1
                    else:
                        error_msg(500)
                        return 0
            else:
                error_msg(500)
                return 0
    else:
        error_msg(500)
        return 0

def data_cmd(line):
    if line[:4] == 'DATA':
        length_np = null_space(line[4:])
        if line[4 + length_np] == '\n':
            correct_data()
            return 1
        else:
            error_msg(500)
            return 0
    else:
        error_msg(500)
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
                length = error_msg(501)
                return length

    else:
        length = error_msg(501)
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
                 length = error_msg(501)
                 return length
        else:
            length = error_msg(501)
            return length
    else:
        length = error_msg(501)
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

def error_msg(num):
    if num == 500:
        print('500 Syntax error: command unrecognized')
    if num == 501:
        print('501 Syntax error in parameters or arguments')
    if num == 503:
        print('503 Bad sequence of commands')
    return 0

def correct_msg():
    print('250 OK')
    return 1

def correct_data():
    print('354 Start mail input; end with <CRLF>.<CRLF>')
    return 1

def check_cmd(line):
    return line[:4]

def recognize_cmd(line):
    if line[:4] == 'MAIL' and line[4+white_space(line[4:]):4+white_space(line[4:])+5] == 'FROM:':
        return True
    elif line[:4] == 'RCPT' and line[4+white_space(line[4:]):4+white_space(line[4:])+3] == 'TO:':
        return True
    elif line[:4] == 'DATA':
        return True
    else:
        return False

import sys
current_state = 'START'
output_value = 0
rcpt_list = []
text = ''
for command in sys.stdin:
    user_input = command
    print(user_input[:-1])
    if current_state == 'START':
        if recognize_cmd(user_input):
            if check_cmd(user_input) == 'MAIL':
                output_value = mail_from(user_input)
                if output_value == 1:
                    who = 'From: <' + from_who(user_input) + '>\n'
                    text += who
                    current_state = 'MAIL'
                    # print(current_state)
                    continue
                else:
                    continue
            else:
                error_msg(503)
                continue
        else:
            error_msg(500)
            continue
    if current_state == 'MAIL':
        if recognize_cmd(user_input):
            if check_cmd(user_input) == 'RCPT':
                output_value = rcpt_to(user_input)
                if output_value == 1:
                    rcpt_list.append(to_who(user_input))
                    who = 'To: <' + to_who(user_input) + '>\n'
                    text += who
                    current_state = 'RCPT'
                    # print(current_state)
                    continue
                else:
                    continue
            else:
                error_msg(503)
                continue
        else:
            error_msg(500)
            continue
    if current_state == 'RCPT':
        if recognize_cmd(user_input):
            if check_cmd(user_input) == 'RCPT':
                output_value = rcpt_to(user_input)
                if output_value == 1:
                    rcpt_list.append(to_who(user_input))
                    who = 'To: <' + to_who(user_input) + '>\n'
                    text += who
                    current_state = 'RCPT'
                    # print(current_state)
                    continue
                else:
                    continue
            elif check_cmd(user_input) == 'DATA':
                output_value = data_cmd(user_input)
                if output_value == 1:
                    current_state = 'DATA'
                    # print(current_state)
                    continue
                else:
                    continue
            else:
                error_msg(503)
                continue
        else:
            error_msg(500)
            continue
    if current_state == 'DATA':
        if user_input == '.\n':
            correct_msg()
            for filename in rcpt_list:
                file = 'forward/'+filename
                with open(file, "a") as f:
                    f.write(text)
            text = ''
            rcpt_list = []
            current_state = 'START'
            #print(current_state)
            continue
        else:
            text += user_input
            continue




