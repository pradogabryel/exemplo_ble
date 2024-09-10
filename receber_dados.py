import asyncio
from bleak import BleakClient

# Endereço MAC 
MAC_ADDRESS = "78:04:73:16:53:2a"  # (AT+LADDR)

# UUID da característica de notificação - possivelmente pedrão para HM-10, mas dá pra obter através do Bluetooth LE Explorer. Utilizar UUID de 128 bits ao invés de 16
CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

# Arquivo para salvar os dados aquisitados
OUTPUT_FILE = "dados_recebidos.txt"

# Callback para processar os dados recebidos e salvar no arquivo
def notification_handler(sender, data):
    try:
        # Decodificar os dados recebidos em UTF-8
        decoded_data = data.decode('utf-8')
        print(f"Notificação de {sender}: {decoded_data}")
        
        # Escrever os dados decodificados no arquivo
        with open(OUTPUT_FILE, "a", encoding='utf-8') as file:
            file.write(f"{decoded_data}\n")
    except UnicodeDecodeError as e:
        print(f"Erro ao decodificar os dados: {e}")

async def main():
    async with BleakClient(MAC_ADDRESS) as client:
        connected = await client.is_connected()
        print(f"Conectado: {connected}")

        # Começar a receber notificações
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

        # Tempo de aquisição
        await asyncio.sleep(120.0)  

        # Parar de receber notificações
        await client.stop_notify(CHARACTERISTIC_UUID)

# Executar o script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
