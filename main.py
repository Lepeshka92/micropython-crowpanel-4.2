import os
import time
import crowpanel

panel = crowpanel.CrowPanel42()

#power led
panel.led.on()

#e-ink display
display = panel.get_display()

#work with framebuffer
display.fill(1)
display.text('Hello, Micropython!', 0, 0, 0)

try:
    #mount sd card
    panel.mount_sdcard('/sd')
except Exception as e:
    display.text('No sd card', 0, 12, 0)
else:
    display.text('Files on sd card:', 0, 12, 0)
    y = 22
    for i,item in enumerate(os.listdir('/sd')):
        display.text('-' + item, 8, y + i * 10, 0)

display.show()

#go to deep sleep
display.sleep()

#exit, home, next, prev, done - buttons
while panel.exit.value():
    time.sleep(0.1)
    print('press exit button!')

panel.led.off()