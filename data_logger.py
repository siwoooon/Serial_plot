try:
    import serial
except ImportError:
    print("Module 'serial' not found. Install pyserial with:\npython -m pip install pyserial")
    raise

import time
import csv
from datetime import datetime

# 1. 설정 (본인 환경에 맞게 수정하세요!)
PORT = 'COM3'   # 장치관리자에서 확인한 포트 번호
BAUDRATE = 115200
FILENAME = datetime.now().strftime("EDA_%Y%m%d_%H%M%S.csv") # 파일명 자동 생성

# 2. 연결/
try:
    ser = serial.Serial(PORT, BAUDRATE)
    print(f"연결 성공! 데이터를 {FILENAME}에 저장합니다... (종료: Ctrl+C)")
except serial.SerialException as e:
    print(f"시리얼 포트를 열 수 없습니다: {e}")
    try:
        from serial.tools import list_ports
        ports = list_ports.comports()
        if ports:
            print("사용 가능한 포트:")
            for p in ports:
                print(" -", p.device)
        else:
            print("사용 가능한 포트가 없습니다.")
    except Exception:
        pass
    raise

# 3. 파일 열고 쓰기
with open(FILENAME, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Resistance(Ohm)"]) # 헤더(제목) 쓰기

    try:
        while True:
            if ser.in_waiting > 0:
                # 보드에서 데이터 한 줄 읽기
                raw_data = ser.readline().decode('utf-8', errors='ignore').strip()

                # 현재 시간 가져오기
                current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

                # 화면에 출력
                print(f"[{current_time}] {raw_data}")

                # CSV 파일에 저장: [시간, 데이터]
                writer.writerow([current_time, raw_data])

    except KeyboardInterrupt:
        print("\n저장 종료!")
    finally:
        try:
            ser.close()
        except Exception:
            pass