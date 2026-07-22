from machine import Pin, PWM
import random
import time

LED1 = 21
LED2 = 20
LED3 = 19
LED4 = 18
LED5 = 17
LED6 = 16
LED7 = 22
LED8 = 15
LED9 = 14
LED10 = 13

BUTTON = 0

led1 = PWM(Pin(LED1))
led2 = PWM(Pin(LED2))
led3 = PWM(Pin(LED3))
led4 = PWM(Pin(LED4))
led5 = PWM(Pin(LED5))
led6 = PWM(Pin(LED6))
led7 = PWM(Pin(LED7))
led8 = PWM(Pin(LED8))
led9 = PWM(Pin(LED9))
led10 = PWM(Pin(LED10))

led1.freq(1000)
led2.freq(1000)
led3.freq(1000)
led4.freq(1000)
led5.freq(1000)
led6.freq(1000)
led7.freq(1000)
led8.freq(1000)
led9.freq(1000)
led10.freq(1000)

button = Pin(BUTTON, Pin.IN, Pin.PULL_UP)

mode = 0
last_button_state = 1
debounce_time = 0

def check_button():
    global mode, last_button_state, debounce_time
    current_state = button.value()
    current_time = time.ticks_ms()
    
    if current_state == 0 and last_button_state == 1:
        if time.ticks_diff(current_time, debounce_time) > 200:
            mode = (mode+1)%5
            debounce_time = current_time
            mode_names = ['Solid', 'Flashing', 'Chase', 'Twinkle', 'Off']
            print(f"Mode: {mode_names[mode]}")
    
    last_button_state = current_state

class States:
    @staticmethod
    def solid_mode():
        led1.duty_u16(65535)
        led2.duty_u16(65535)
        led3.duty_u16(65535)
        led4.duty_u16(65535)
        led5.duty_u16(65535)
        led6.duty_u16(65535)
        led7.duty_u16(65535)
        led8.duty_u16(65535)
        led9.duty_u16(65535)
        led10.duty_u16(65535)
        time.sleep(0.05)

    @staticmethod
    def flashing_mode():
        for duty in range(0, 65536, 512):
            led1.duty_u16(duty)
            led2.duty_u16(65535-duty)
            led3.duty_u16(duty)
            led4.duty_u16(65535-duty)
            led5.duty_u16(duty)
            led6.duty_u16(65535-duty)
            led7.duty_u16(duty)
            led8.duty_u16(65535-duty)
            led9.duty_u16(duty)
            led10.duty_u16(65535-duty)

            time.sleep(0.005)
            check_button()
            if mode != 1:
                return
        
        for duty in range(65535, -1, -512):
            led1.duty_u16(duty)
            led2.duty_u16(65535-duty)
            led3.duty_u16(duty)
            led4.duty_u16(65535-duty)
            led5.duty_u16(duty)
            led6.duty_u16(65535-duty)
            led7.duty_u16(duty)
            led8.duty_u16(65535-duty)
            led9.duty_u16(duty)
            led10.duty_u16(65535-duty)

            time.sleep(0.005)
            check_button()
            if mode != 1:
                return

    @staticmethod    
    def chase_mode():
        leds = [led1, led2, led3, led4, led5, led6, led7, led8, led9, led10]
        
        while mode == 2:
            for i in range(len(leds)):
                if mode != 2:
                    return

                for brightness in range(0, 65536, 1000):
                    leds[i].duty_u16(brightness)
                    time.sleep(0.003)
                    check_button()
                    if mode != 2:
                        return

                for brightness in range(65535, -1, -1000):
                    leds[i].duty_u16(brightness)
                    time.sleep(0.003)
                    check_button()
                    if mode != 2:
                        return

    @staticmethod
    def off():
        leds = [led1, led2, led3, led4, led5, led6, led7, led8, led9, led10]
        for led in leds:
            led.duty_u16(0)
        time.sleep(0.05)
        
    @staticmethod
    def twinkle():
        leds = [led1, led2, led3, led4, led5, led6, led7, led8, led9, led10]
        lastLED = []
        
        for led in leds:
            led.duty_u16(500)

        while mode == 3:
            rand_led = random.choice(leds)
            rand_brightness = random.randrange(10000, 60000)
            
            if rand_led in lastLED:
                continue
            else:
                for brightness in range(0, rand_brightness, 500):
                    rand_led.duty_u16(brightness)
                    time.sleep(0.01)
                    check_button()
                    if mode != 3:
                        return

                for brightness in range(rand_brightness, 0, -500):
                    rand_led.duty_u16(brightness)
                    time.sleep(0.01)
                    check_button()
                    if mode != 3:
                        return

                lastLED.append(rand_led)

                if len(lastLED) > 5:
                    lastLED.pop(0)

try:
    print("Starting - Mode: Solid")
    while True:
        check_button()
        
        if mode == 0:
            States.solid_mode()
        elif mode == 1:
            States.flashing_mode()
        elif mode == 2:
            States.chase_mode()
        elif mode == 3:
            States.twinkle()
        else:
            States.off()
            
except KeyboardInterrupt:
    leds = [led1, led2, led3, led4, led5, led6, led7, led8, led9, led10]
    for led in leds:
        led.duty_u16(0)
        led.deinit()
    
    print("LED PWM stopped")

