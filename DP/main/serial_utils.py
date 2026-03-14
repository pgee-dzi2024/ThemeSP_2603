# controller/serial_utils.py
import serial
import time

# Настройки на порта (промени COM3 с твоя порт, напр. COM4, COM5 или /dev/ttyUSB0)
PORT = 'COM3'
BAUD_RATE = 9600

# Глобална променлива, която ще държи порта отворен
_serial_conn = None


def get_connection():
    global _serial_conn
    # Ако няма връзка или е затворена, опитваме да я отворим
    if _serial_conn is None or not _serial_conn.is_open:
        try:
            _serial_conn = serial.Serial(PORT, BAUD_RATE, timeout=2)
            # Когато се отвори сериен порт, Arduino се рестартира. Чакаме 2 секунди да зареди.
            time.sleep(2)
        except Exception as e:
            print(f"Грешка при свързване: {e}")
            return None
    return _serial_conn


def send_command_to_arduino(command_char):
    """
    Изпраща символ към Arduino и връща отговора.
    command_char трябва да е '1', '0' или '?'
    """
    conn = get_connection()
    if not conn:
        return {"success": False, "error": "Няма връзка с хардуера"}

    try:
        # Изпращаме командата като байтове
        conn.write(command_char.encode('utf-8'))

        # Четем отговора до получаване на нов ред
        response = conn.readline().decode('utf-8').strip()

        if response:
            return {"success": True, "data": response}
        else:
            return {"success": False, "error": "Устройството не отговори"}

    except Exception as e:
        # Ако връзката прекъсне (напр. изваден кабел)
        global _serial_conn
        if _serial_conn:
            _serial_conn.close()
            _serial_conn = None
        return {"success": False, "error": str(e)}