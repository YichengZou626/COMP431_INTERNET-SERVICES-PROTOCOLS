def from_who(line):
    length_wp = white_space(line[5:])
    length_path = reverse_path(line[5 + length_wp:])
    return line[5 + length_wp: 5 + length_wp + length_path]

def to_who(line):
    length_wp = white_space(line[3:])
    length_path = reverse_path(line[3+length_wp:])
    return line[3 + length_wp: 3 + length_wp + length_path]

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

def check_cmd(line):
    if line[:5] == "From:":
        return line[:4]
    elif line[:3] == 'To:':
        return line[:2]
    else:
        return "text"

def check_rsp(line):
    if line[:3] == '250':
        if white_space(line[3:]) != 0:
            if is_string(line[3+white_space(line[3:]):]) > 0:
                return True
    return False

def check_data(line):
    if line[:3] == '354':
        if white_space(line[3:]) != 0:
            if is_string(line[3+white_space(line[3:]):]) > 0:
                return True
    return False

def check_error(line):
    if line[:3] == '500' or line[:3] == '501':
        if white_space(line[3:]) != 0:
            if is_string(line[3+white_space(line[3:]):]) > 0:
                return True
    return False




import sys
current_state = 'START'
error = False
filename = sys.argv[1]
with open(filename, 'r') as f:
    Lines = f.readlines()
    for line in Lines:
        user_input = line
        if current_state == 'START':
            if check_cmd(user_input) == "From":
                print('MAIL FROM: ' + from_who(user_input))
                current_state = 'MAIL'
                output = input()
                sys.stderr.write(output + '\n')
                if check_rsp(output):
                    continue
                else:
                    print('QUIT')
                    error = True
                    break
        if current_state == 'MAIL':
            if check_cmd(user_input) == "To":
                print('RCPT TO: ' + to_who(user_input))
                current_state = 'RCPT'
                output = input()
                sys.stderr.write(output + '\n')
                if check_rsp(output):
                    continue
                else:
                    print('QUIT')
                    error = True
                    break
        if current_state == 'RCPT':
            if check_cmd(user_input) == 'From':
                print('DATA')
                output = input()
                sys.stderr.write(output + '\n')
                if check_data(output):
                    print('.')
                    output = input()
                    sys.stderr.write(output + '\n')
                    if check_rsp(output):
                        print('MAIL FROM: ' + from_who(user_input))
                        output = input()
                        sys.stderr.write(output + '\n')
                        if check_rsp(output):
                            continue
                        else:
                            print('QUIT')
                            error = True
                            break
                    else:
                        print('QUIT')
                        error = True
                        break
                else:
                    print('QUIT')
                    error = True
                    break
            if check_cmd(user_input) == 'To':
                print('RCPT TO: ' + to_who(user_input))
                current_state = 'RCPT'
                output = input()
                sys.stderr.write(output + '\n')
                if check_rsp(output):
                    continue
                else:
                    print('QUIT')
                    error = True
                    break
            if check_cmd(user_input) == "text":
                print('DATA')
                current_state = 'DATA'
                output = input()
                sys.stderr.write(output + '\n')
                if check_data(output):
                    if user_input[-1] != '\n':
                        print(user_input)
                    else:
                        print(user_input[:-1])
                    continue
                else:
                    print('QUIT')
                    error = True
                    break
        if current_state == 'DATA':
            if check_cmd(user_input) == "text":
                current_state = 'DATA'
                if user_input[-1] != '\n':
                    print(user_input)
                else:
                    print(user_input[:-1])
                continue
            if check_cmd(user_input) == 'From':
                print('.')
                output = input()
                sys.stderr.write(output + '\n')
                if check_rsp(output):
                    print('MAIL FROM: ' + from_who(user_input))
                    current_state = 'MAIL'
                    output = input()
                    sys.stderr.write(output + '\n')
                    if check_rsp(output):
                        continue
                    else:
                        print('QUIT')
                        error = True
                        break
                else:
                    print('QUIT')
                    error = True
                    break
    if not error:
        if current_state == 'RCPT':
            print('DATA')
            output = input()
            sys.stderr.write(output + '\n')
            if not check_data(output):
                print('QUIT')

                sys.exit()
        print('.')
        output = input()
        sys.stderr.write(output + '\n')
        print('QUIT')
        f.close()

