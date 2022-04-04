def mail_from(line):
    if line[:4] == 'MAIL':
        length_wp = white_space(line[4:])
        if length_wp == 0:
            error_msg('mail_from_cmd')
            return
        else:
            if line[4+length_wp:4+length_wp+5] == 'FROM:':
                length_null = null_space(line[4+length_wp+5:])
                length_path = reverse_path(line[4+length_wp+5+length_null:])
                if length_path == 0:
                    return
                else:
                    length_nul = null_space(line[4+length_wp+5+length_null+length_path:])
                    if line[4+length_wp+5+length_null+length_path+length_nul] == '\n':
                        correct_msg()
                        return
                    else:
                        error_msg('mail_from_cmd')
                        return
            else:
                error_msg('mail_from_cmd')
                return
    else:
        error_msg('mail_from_cmd')
        return

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
                length = error_msg('path')
                return length

    else:
        length = error_msg('path')
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
                 length = error_msg('mailbox')
                 return length
        else:
            length = error_msg('mailbox')
            return length
    else:
        length = error_msg('mailbox')
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

def error_msg(line):
    print('ERROR -- '+line)
    return 0

def correct_msg():
    print('Sender ok')
    return 1


import sys

for command in sys.stdin:
    user_input = command
    print(user_input[:-1])
    mail_from(user_input)

