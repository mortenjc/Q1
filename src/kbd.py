import sys
import termios
from select import select
#from enum import Enum

# class kMBP(Enum):
#     optb = 0x222b
#     optc = 231
#     optg = 169
#     optm = 181
#     backspace = 127
#
# q1key = {
#     "GO"   : kMBP.optg,
#     "CORR" : kMBP.backspace,
#     "CLEAR ENTRY" : kMBP.optc,
#     "INSERT MODE" : kMBP.optm
# }



class Key:

    def __init__(self):
        # save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # new terminal setting unbuffered
        self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)


    def __del__(self):
        # switch to normal terminal
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def putch(self, ch):
        sys.stdout.write(ch)

    def getch(self):
        return sys.stdin.read(1)

    def getche(self):
        ch = self.getch()
        self.putch(ch)
        return ch

    def kbhit(self):
        dr,_,_ = select([sys.stdin], [], [], 0)
        return dr != []

if __name__ == '__main__':

    kbd = Key()

    while 1:
        if kbd.kbhit():
            char = kbd.getch()
            break
        print("A")
        #sys.stdout.write('.')

    print(f'done {char}')
