import curses
import socket

stdscr = curses.initscr()
curses.resize_term(26, 42)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def main(stdscr):
    stdscr.clear()
    stdscr.border()
    curses.curs_set(1)

    stdscr.addstr(10, 1, '  Q1 display emulator')
    stdscr.refresh()

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        x = int(data[0])
        y = int(data[1])
        data = data[2:]
        for i in range(24):
            line = data[i*40:i*40+40]
            stdscr.addstr(i+1, 1, '{}'.format(line.decode('utf-8')))
        stdscr.move(y+1,x)
        stdscr.refresh()

curses.wrapper(main)
