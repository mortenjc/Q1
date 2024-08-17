import curses
import socket
#from curses import wrapper
stdscr = curses.initscr()

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))



def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(1, 11):
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(i, 10/i))
    stdscr.refresh()

    while True:
        # data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        # print("received message: %s" % data)

        stdscr.refresh()
        k = stdscr.getkey()
        if k == 'q':
            return
        stdscr.addstr(20, 0, f'key  {k}')

curses.wrapper(main)
