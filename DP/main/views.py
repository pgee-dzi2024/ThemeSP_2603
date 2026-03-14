from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serial_utils import send_command_to_arduino

def index(request):
    return render(request, 'main/index.html')





@api_view(['GET', 'POST'])
def device_control(request):
    # GET заявка - използваме я за проверка на текущия статус
    if request.method == 'GET':
        result = send_command_to_arduino('?')
        if result['success']:
            return Response({"status": "ok", "device_state": result['data']})
        return Response({"status": "error", "message": result['error']}, status=503)

    # POST заявка - използваме я за включване/изключване
    if request.method == 'POST':
        # Вземаме желаната команда от заявката
        command = request.data.get('command')

        # Валидиране на командата (Изискване по задание)
        if command not in ['ON', 'OFF']:
            return Response({"status": "error", "message": "Невалидна команда. Използвайте 'ON' или 'OFF'."},
                            status=400)

        # Превеждаме уеб командата към хардуерна команда
        hardware_cmd = '1' if command == 'ON' else '0'

        # Изпращаме към Arduino
        result = send_command_to_arduino(hardware_cmd)

        if result['success']:
            return Response({"status": "ok", "device_response": result['data']})
        else:
            return Response({"status": "error", "message": result['error']}, status=503)