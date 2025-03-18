import serial
import threading
import tkinter as tk
from tkinter import messagebox
import json
import math
import pymysql
from datetime import datetime

arduino = None
serial_thread = None  

def open_serial():
    global arduino, serial_thread
    try:
        # 시리얼 포트 경로를 /dev/ttyUSB0로 변경합니다.
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        text_box.insert(tk.END, "Serial port opened.\n")
        text_box.see(tk.END)
        
        serial_thread = threading.Thread(target=read_from_arduino)
        serial_thread.daemon = True
        serial_thread.start()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open serial port: {e}")

def close_serial():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        text_box.insert(tk.END, "Serial port closed.\n")
        text_box.see(tk.END)
        # 시리얼 포트 닫은 후 변수 초기화
        arduino = None
    else:
        messagebox.showinfo("Info", "Serial port is already closed.")

def read_from_arduino():
    global arduino
    while True:
        # 아두이노 객체가 없거나 열려있지 않으면 루프 종료
        if not arduino or not arduino.is_open:
            break

        try:
            bytes_waiting = arduino.in_waiting
        except (OSError, TypeError) as e:
            text_box.insert(tk.END, f"Serial error reading in_waiting: {e}\n")
            text_box.see(tk.END)
            break  # 오류 발생 시 루프 종료
        
        if bytes_waiting > 0:
            try:
                data = arduino.readline().decode('utf-8', errors='ignore').strip()
            except Exception as e:
                text_box.insert(tk.END, f"Error reading line: {e}\n")
                text_box.see(tk.END)
                continue

            try:
                json_data = json.loads(data)
                text_box.insert(tk.END, f"Received JSON: {json_data}\n")
                mydist = round(json_data.get('dist', 0), 2)
                label1.config(text=f"거리값 = {mydist} cm")
                insert_data(mydist)
            except json.JSONDecodeError:
                text_box.insert(tk.END, f"Received (not JSON): {data}\n")
            except Exception as e:
                text_box.insert(tk.END, f"Error processing data: {e}\n")
            
            text_box.see(tk.END)

def send_to_arduino():
    global arduino
    if arduino and arduino.is_open:
        arduino.write(b'test\n')
        text_box.insert(tk.END, "Sent: test\n")
        text_box.see(tk.END)
    else:
        messagebox.showinfo("Info", "Serial port is not open.")

def insert_data(distance):
    try:
        conn = pymysql.connect(
            host="localhost", 
            user="arduino", 
            password="123f5678", 
            database="python30",
            charset='utf8mb4'
        )
        conn.autocommit(True)
        cursor = conn.cursor()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO distance_data (distance, date) VALUES (%s, %s)"
        cursor.execute(sql, (distance, current_time))
        
        cursor.close()
        conn.close()
        print("Data inserted successfully!")
    except pymysql.MySQLError as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

root = tk.Tk()
root.title("Arduino Serial Communication")
root.geometry("700x300")

text_box = tk.Text(root, height=10, width=80)
text_box.pack()

label1 = tk.Label(root, text="값 없음!", font=("Arial", 20))
label1.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

open_button = tk.Button(frame, text="Open Serial Port", command=open_serial)
open_button.pack(side=tk.LEFT, padx=5)

close_button = tk.Button(frame, text="Close Serial Port", command=close_serial)
close_button.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(frame, text="Send 'test'", command=send_to_arduino)
send_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
