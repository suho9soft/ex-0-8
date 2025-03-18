import machine
import time

# 각 버튼과 LED가 연결된 GPIO 핀 설정
button_pins = [15, 14, 13, 12]  # 버튼이 연결된 핀
led_pins = [18, 19, 20, 21]  # LED가 연결된 핀

# 버튼 상태를 추적하는 변수 (각 LED의 켜짐/꺼짐 상태)
led_states = [False, False, False, False]

# 각 버튼과 LED 핀을 초기화
buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in button_pins]
leds = [machine.Pin(pin, machine.Pin.OUT) for pin in led_pins]

def toggle_led(button_index):
    # LED의 상태를 반전시킴
    led_states[button_index] = not led_states[button_index]
    leds[button_index].value(1 if led_states[button_index] else 0)  # LED를 켜거나 끔

# 이전 버튼 상태를 추적하는 변수 (디바운싱을 위해 사용)
prev_button_states = [True, True, True, True]

while True:
    for i, button in enumerate(buttons):
        # 버튼의 현재 상태
        current_button_state = button.value()
        
        # 버튼이 눌린 상태에서만 처리 (디바운싱 고려)
        if current_button_state == 0 and prev_button_states[i] == 1:
            toggle_led(i)  # 버튼에 해당하는 LED 상태 변경
        
        # 현재 버튼 상태를 이전 상태로 저장
        prev_button_states[i] = current_button_state
    
    time.sleep(0.1)  # 100ms 대기하여 디바운싱 처리
