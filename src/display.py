import socket

'''
    Display emulator for Q1
'''


def txudp(message):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))


class Display:

    def __init__(self, height=24, width=40):
        self.w = width
        self.h = height
        self.pos = (0,0)
        self.buffer = [[chr(0x20) for x in range(width)] for y in range(height)]


    def _incx(self):
        x, y = self.pos
        x += 1
        if x == self.w:
            x = 0
            y += 1
        if y == self.h:
            #print('y exceeds maximum')
            y = 0
        self.pos = (x,y)


    def data(self, char):
        if 32 <= ord(char) < 127:
            x, y = self.pos
            self.buffer[y][x] = char
        self._incx()


    def control(self, val):
        x, y = self.pos
        reset   = val & 0x01
        blank   = val & 0x02
        unblank = val & 0x04
        step    = val & 0x08

        if reset:
            self.pos = (0,0)
        elif step:
            self._incx()


    def update(self):
        msg = chr(self.pos[0]) + chr(self.pos[1])
        for l in self.buffer:
            msg += ''.join(l)
        txudp(msg)

if __name__ == '__main__':
    import time
    d = Display()
    while True:
        d.data('a')
        d.update()
        time.sleep(1)
