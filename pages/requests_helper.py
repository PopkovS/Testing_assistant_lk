import re
import socket

from pages.locators import TestData


def request_sending_edit_user(my_filename='edit_user', id_user='144', email=TestData.TEST_USER, status_id="0",
                              two_factor="False"):
    with open(fr'../packages/{my_filename}.txt', 'rb+') as fp:
        pack_read = fp.read()
        old_id = re.search(r"name=\"Id\"\r\n\r\n(\d*)\r\n", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_id}', f"name=\"Id\"\r\n\r\n{id_user}\r\n", pack_read.decode("utf-8"))

        old_email = re.search(r"name=\"Email\"\r\n\r\n(.*@.*)\r\n", pack_read.decode("utf-8")).group(1)
        new_pack = re.sub(fr'{old_email}', email, new_pack)

        old_status_id = re.search(r"name=\"StatusId\"\r\n\r\n\d", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_status_id}', f"name=\"StatusId\"\r\n\r\n{status_id}", new_pack)

        old_two_factor = re.search(r"name=\"TwoFactor\"\r\n\r\n\w{4,5}", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_two_factor}', f"name=\"TwoFactor\"\r\n\r\n{two_factor}", new_pack)

        open(fr'../packages/{my_filename}.txt', 'w').close()
        fp.seek(0)
        fp.write(new_pack.encode("utf-8"))


def send_pack(pak_name, dot=".*"):
    sock = sock_connect()
    sock.sendall(open(rf'{dot}/packages/{pak_name}.txt', 'rb').read())
    print_response(sock)


def sock_connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('192.168.71.2', 80))
    return sock


def print_response(sock):
    data = sock.recv(1024).decode("utf-8", errors="replace")
    sock.close()
    print(data)


def recount_length(my_filename):
    with open(fr'../packages/{my_filename}.txt', 'rb+') as fp:
        pack_read = fp.read()
        length_old = re.search(r'Content-Length: (\d*)', pack_read.decode("utf-8")).group(1)
        length_new = len(pack_read[1137:])
        new_pack = re.sub(fr'{length_old}', f'{length_new}', pack_read.decode("utf-8"))
        open(fr'../packages/{my_filename}.txt', 'w').close()
        fp.seek(0)
        fp.write(new_pack.encode("utf-8"))
