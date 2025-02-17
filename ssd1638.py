from time import sleep_ms
from machine import SPI, Pin
from framebuf import FrameBuffer, MONO_HLSB


class SSD1638(FrameBuffer):

    def __init__(self, width=400, height=300, cs=45, dc=46, rst=47, busy=48, spi_id=1, sck=12, mosi=11):
        self._w = width
        self._h = height
        self._buf = bytearray(width * height // 8)
        super().__init__(self._buf, width, height, MONO_HLSB)
        
        self._cs = Pin(cs, Pin.OUT)
        self._dc = Pin(dc, Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
        self._busy = Pin(busy, Pin.IN)
        
        self._spi = SPI(spi_id,
                        baudrate=4_000_000,
                        sck=Pin(sck),
                        mosi=Pin(mosi),
                        firstbit=SPI.MSB)
        self.init()

    def _cmd(self, b):
        self._cs(0)
        self._dc(0)
        self._spi.write(bytearray([b]))
        self._cs(1)

    def _dat(self, b):
        self._cs(0)
        self._dc(1)
        self._spi.write(bytearray([b]))
        self._cs(1)

    def _wait(self):
        while self._busy.value() == 1:
            sleep_ms(1)

    def _reset(self):
        self._rst.value(0)
        sleep_ms(10)
        self._rst.value(1)
        sleep_ms(10)

    def _pos(self, x1, y1, x2, y2):
        self._cmd(0x44)
        self._dat((x1 >> 3) & 0xFF)
        self._dat((x2 >> 3) & 0xFF)

        self._cmd(0x45)
        self._dat(y1 & 0xFF)
        self._dat((y1 >> 8) & 0xFF)
        self._dat(y2 & 0xFF)
        self._dat((y2 >> 8) & 0xFF)

    def _cur(self, x, y):
        self._cmd(0x4E)
        self._dat(x & 0xFF)

        self._cmd(0x4F)
        self._dat(y & 0xFF)
        self._dat((y >> 8) & 0xFF)

    def _update(self):
        self._cmd(0x22)
        self._dat(0xF7)
        self._cmd(0x20)
        self._wait()

    def init(self):
        self._reset()
        self._wait()
        
        self._cmd(0x12)
        self._wait()
        
        self._cmd(0x21)
        self._dat(0x40)
        self._dat(0x00)
        self._cmd(0x3C)
        self._dat(0x05)

#       self._cmd(0x1A)
#       self._dat(0x5A)
#
#       self._cmd(0x22)
#       self._dat(0x91)
#       self._cmd(0x20)
#       self._wait()

        self._cmd(0x11)
        self._dat(0x03)
        self._pos(0, 0, self._w - 1, self._h - 1)
        self._cur(0, 0)
        self._wait()

    def sleep(self):
        self._cmd(0x10)
        self._dat(0x01)
        sleep_ms(100)

    def show(self):
        self._cmd(0x24)
        self._cs(0)
        self._dc(1)
        self._spi.write(self._buf)
        self._cs(1)
        self._update()