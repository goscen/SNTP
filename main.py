import socket
import datetime
import argparse
import struct
from multiprocessing.pool import ThreadPool

TIME = datetime.datetime(1900, 1, 1)


def send_packet(input_packet, address, sock, receive_time):
    packet = struct.pack('!B', 28) + struct.pack('!B', 1) \
             + struct.pack('!b', 0) + struct.pack('!b', -20) + struct.pack('!i', 0) \
             + struct.pack('!i', 0) + struct.pack('!i', 0) \
             + get_time() + input_packet[40:48] + receive_time
    sock.sendto(packet + get_time(), address)


def get_time():
    time = (datetime.datetime.utcnow() - TIME).total_seconds() + my_delay
    seconds, milliseconds = [int(x) for x in str(time).split('.')]
    return struct.pack('!II', seconds, milliseconds)


def start_work():
    print("Server is running")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", my_port))
    # 10 потоков
    thread_pool = ThreadPool(processes=10)
    while True:
        data, addr = sock.recvfrom(1024)
        print(f'{addr[0]} connected')
        receive_time = get_time()
        thread_pool.apply_async(send_packet, args=(data, addr, sock, receive_time))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest="delay", type=int, default=0)
    parser.add_argument('-p', '--port', dest="port", type=int, default=123)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    my_delay = args.delay
    my_port = args.port
    start_work()
