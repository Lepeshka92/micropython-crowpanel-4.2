from machine import Pin, SDCard

SSD1638_WIDTH  = const(400)
SSD1638_HEIGHT = const(300)

SSD1638_PWR    = const(7)
SSD1638_CS     = const(45)
SSD1638_DC     = const(46)
SSD1638_RST    = const(47)
SSD1638_BUSY   = const(48)

SSD1638_SPI    = const(1)
SSD1638_SCK    = const(12)
SSD1638_MOSI   = const(11)

SDCARD_SLOT    = const(2)
SDCARD_PWR     = const(42)
SDCARD_CS      = const(10)
SDCARD_MOSI    = const(40)
SDCARD_CLK     = const(39)
SDCARD_MISO    = const(13)

KEY_HOME       = const(2)
KEY_EXIT       = const(1)
KEY_PREV       = const(6)
KEY_NEXT       = const(4)
KEY_DONE       = const(5)
POWER_LED      = const(41)

class CrowPanel42(object):

    def __init__(self):
        self._display = None
        self.home = Pin(KEY_HOME, Pin.IN)
        self.exit = Pin(KEY_EXIT, Pin.IN)
        self.prev = Pin(KEY_PREV, Pin.IN)
        self.done = Pin(KEY_DONE, Pin.IN)
        self.next = Pin(KEY_NEXT, Pin.IN)
        self.led = Pin(POWER_LED, Pin.OUT)

    def get_display(self):
        if self._display is None:
            import ssd1638
            Pin(SSD1638_PWR, Pin.OUT, value=1)
            self._display = ssd1638.SSD1638(SSD1638_WIDTH,
                                            SSD1638_HEIGHT,
                                            SSD1638_CS,
                                            SSD1638_DC,
                                            SSD1638_RST,
                                            SSD1638_BUSY,
                                            SSD1638_SPI,
                                            SSD1638_SCK,
                                            SSD1638_MOSI)
        return self._display

    def mount_sdcard(self, path):
        import vfs
        Pin(SDCARD_PWR, Pin.OUT, value=1)
        sd = SDCard(slot=SDCARD_SLOT,
                    sck=SDCARD_CLK,
                    miso=SDCARD_MISO,
                    mosi=SDCARD_MOSI,
                    cs=SDCARD_CS)
        vfs.mount(sd, path)