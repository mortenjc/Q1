#include </Users/mortenchristensen/projects/z80/z80.h>
#include <string>

#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

// kbhit
using z80::fast_u8;
using z80::fast_u16;
using z80::least_u8;


int kbhit(void)
{
  struct termios oldt, newt;
  int ch, oldf;

  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

  ch = getchar();

  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  fcntl(STDIN_FILENO, F_SETFL, oldf);

  if(ch != EOF) {
    ungetc(ch, stdin);
    return 1;
  }

  return 0;
}
// kbhit - end


class my_emulator : public z80::z80_cpu<my_emulator> {
public:
    int icount{0};
    bool verbose{true};
    typedef z80::z80_cpu<my_emulator> base;

    my_emulator() {}

    void on_set_pc(fast_u16 pc) {
        base::on_set_pc(pc);
    }

    // void on_decode(fast_u8 op) {
    //   printf("opc 0x%02x\n", op);
    //   base::on_decode(op);
    // }


    void on_step() {
        unsigned pc = static_cast<unsigned>(get_pc());
        unsigned a = static_cast<unsigned>(get_a());
        unsigned bc = static_cast<unsigned>(get_bc());
        unsigned de = static_cast<unsigned>(get_de());
        unsigned hl = static_cast<unsigned>(get_hl());
        uint8_t flg = static_cast<uint8_t>(get_f());
        std::string flags{""};
        std::string sep{"."};
        (flg & sf_mask) ? flags += "s" : flags+=sep;
        (flg & zf_mask) ? flags += "z" : flags+=sep;
        (flg & yf_mask) ? flags += "y" : flags+=sep;
        (flg & hf_mask) ? flags += "h" : flags+=sep;
        (flg & xf_mask) ? flags += "x" : flags+=sep;
        (flg & pf_mask) ? flags += "p" : flags+=sep;
        (flg & nf_mask) ? flags += "n" : flags+=sep;
        (flg & zf_mask) ? flags += "z" : flags+=sep;

        if (verbose) {
          std::printf("%04x: %02x .. .. .. ;       |a:%02x, bc:%04x, de:%04x, hl:%04x | flags %s\n",
            pc, memory[pc], a, bc, de, hl, flags.c_str());
        }
        base::on_step();
    }

    fast_u8 on_read(fast_u16 addr) {
        assert(addr < z80::address_space_size);
        fast_u8 n = memory[addr];
        // std::printf("read 0x%02x at 0x%04x\n", static_cast<unsigned>(n),
        //             static_cast<unsigned>(addr));
        return n;
    }

    void on_write(fast_u16 addr, fast_u8 n) {
        assert(addr < z80::address_space_size);
        std::printf("write 0x%02x at 0x%04x\n", static_cast<unsigned>(n),
                    static_cast<unsigned>(addr));
        memory[addr] = static_cast<least_u8>(n);
    }

    // fast_u8 on_input(fast_u16 port) {
    //     fast_u8 n = 0xfe;
    //     std::printf("input 0x%02x from 0x%04x\n", static_cast<unsigned>(n),
    //                 static_cast<unsigned>(port));
    //     return n;
    // }

    // void on_output(fast_u16 port, fast_u8 n) {
    //     std::printf("output 0x%02x to 0x%04x\n", static_cast<unsigned>(n),
    //                 static_cast<unsigned>(port));
    // }

private:
    least_u8 memory[z80::address_space_size] = {
      0x11, 0xff, 0xff,  // ld de ffff
      0x1b,              // dec de
      0x7a,              // ld a,d
      0xb3,              // or e
      0xc2, 0x03, 0x00,  // jp nz 0003
      0xc3, 0x00, 0x00   // jp 0000
    };
};

int main() {
    my_emulator e;

    while (true) {
      e.on_step();
      if (kbhit()) {
         int ch = getchar();
         printf("handle key %d (0x%02x)\n", ch, ch);
         if (ch == 27) { // ESC
           break;
         } else if (ch == 128) { // option-p
           //printf("verbose %d\n", verbose);
           e.verbose ^= 1;
         }
      }
    }
}
