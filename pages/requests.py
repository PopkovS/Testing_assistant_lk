import re
import socket

from .locators import TestData


def request_sending_edit_user(my_filename='editUser1091', email=TestData.TEST_USER, status_id="0", two_factor="False"):
    with open(fr'./packages/{my_filename}.txt', 'rb+') as fp:
        pack_read = fp.read()
        print(pack_read)
        length_old = re.search(r'Content-Length: (.*)', pack_read.decode("utf-8")).group(1)

        old_email = re.search(r"name=\"Email\"\r\n\r\n(.*@.*)\r\n", pack_read.decode("utf-8")).group(1)
        new_pack = re.sub(fr'{old_email}', email, pack_read.decode("utf-8"))
        old_status_id = re.search(r"name=\"StatusId\"\r\n\r\n\d", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_status_id}', f"name=\"StatusId\"\r\n\r\n{status_id}", new_pack)

        old_two_factor = re.search(r"name=\"TwoFactor\"\r\n\r\n\w{4,5}", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_two_factor}', f"name=\"TwoFactor\"\r\n\r\n{two_factor}", new_pack)

        length_new = len(new_pack.encode("utf-8")[1091:])
        new_pack = re.sub(fr'{length_old}', f'{length_new}', new_pack)
        open(fr'./packages/{my_filename}.txt', 'w').close()
        fp.seek(0)
        fp.write(new_pack.encode("utf-8"))

    sock = sock_connect()
    send_pack('loginUser')
    send_pack(f'{my_filename}')
    send_pack('logout')

    # print_response(sock)


def send_pack(pak_name):
    sock = sock_connect()
    sock.sendall(open(rf'./packages/{pak_name}.txt', 'rb').read())
    print_response(sock)


def sock_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.71.2', 80))
    return sock


def print_response(sock):
    data = sock.recv(1024).decode("utf-8", errors="replace")
    sock.close()
    print(data)
