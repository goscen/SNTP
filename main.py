import argparse
import socket
import struct
import threading
import time


def craft_and_send_ntp_packet(sock: socket, addr, delay):
    current_time = time.time()
    current_time += delay
    li_vn_mode = (0 << 6) | (4 << 3) | 4  # LI = 0, VN = 4, Mode = 4 (server)
    """
    stratum = 0, pool = 0, precision = -6, root_delay = 0, root_dispersion = 0,
    ref_id = 2130706433(127.0.0.1)
    """
    packet = struct.pack("!BBBb11I", li_vn_mode, 0, 0, -6, 0, 0, 2130706433, int(current_time),
                         int((current_time - int(current_time)) * 2 ** 32))
    sock.sendto(packet, addr)


def start_server(delay, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", port))
    print("server starts to work")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Work with {addr}")
        t = threading.Thread(target=craft_and_send_ntp_packet, args=(sock, addr, delay))
        t.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--delay", type=int, default=0)
    parser.add_argument("-p", "--port", type=int, default=123)
    args = parser.parse_args()
    start_server(args.delay, args.port)
