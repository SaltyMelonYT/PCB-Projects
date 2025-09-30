from machine import Pin, PWM
import time

# Configure GPIO pins
LED1 = 0
LED2 = 1
LED3 = 2
LED4 = 3
LED5 = 4
LED6 = 5
LED7 = 6
LED8 = 7
LED9 = 8
LED10 = 9

BUTTON = 22  # Change to your button GPIO pin

# Set up PWM for LEDs
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


# Set up button with internal pull-up resistor
button = Pin(BUTTON, Pin.IN, Pin.PULL_UP)

# Mode variable: 0 = solid, 1 = flashing, 2 = chase
mode = 0
last_button_state = 1
debounce_time = 0

def check_button():
    global mode, last_button_state, debounce_time
    current_state = button.value()
    current_time = time.ticks_ms()
    
    # Button pressed (goes LOW when pressed with pull-up)
    if current_state == 0 and last_button_state == 1:
        if time.ticks_diff(current_time, debounce_time) > 200:  # 200ms debounce
            mode = (mode+1)%3  # Toggle between 0 and 2
            debounce_time = current_time
            mode_names = ['Solid', 'Flashing', 'Chase']
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
        # Fade in
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

            time.sleep(0.01)
            check_button()
            if mode != 1:  # Mode changed, exit
                return
        
        # Fade out
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

            time.sleep(0.01)
            check_button()
            if mode != 1:  # Mode changed, exit
                return

    @staticmethod    
    def chase_mode():
        leds = [led1, led2, led3, led4, led5, led6, led7, led8, led9, led10]
        
        while True:
            for i in range(len(leds)):
                # Turn off all LEDs
                for led in leds:
                    led.duty_u16(0)
                
                # Turn on current LED
                leds[i].duty_u16(65535)
                
                time.sleep(0.1)
                check_button()
                if mode != 2:
                    return


# Main loop
try:
    print("Starting - Mode: Solid")
    while True:
        check_button()
        
        if mode == 0:
            States.solid_mode()
        elif mode == 1:
            States.flashing_mode()
        else:
            States.chase_mode()
            
except KeyboardInterrupt:
    # Clean up on exit
    led1.duty_u16(0)
    led2.duty_u16(0)
    led3.duty_u16(0)
    led4.duty_u16(0)
    led5.duty_u16(0)
    led6.duty_u16(0)
    led7.duty_u16(0)
    led8.duty_u16(0)
    led9.duty_u16(0)
    led10.duty_u16(0)

    led1.deinit()
    led2.deinit()
    led3.deinit()
    led4.deinit()
    led5.deinit()
    led6.deinit()
    led7.deinit()
    led8.deinit()
    led9.deinit()
    led10.deinit()

    print("LED PWM stopped")