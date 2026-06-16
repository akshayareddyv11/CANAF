from netmiko import ConnectHandler

device = {
    "device_type": "cisco_xe",
    "host": "10.10.20.48",
    "username": "developer",
    "password": "C1sco12345",
    "port": 22,
}

try:
    connection = ConnectHandler(**device)
    print("Connected Successfully!")

    running_config = connection.send_command("show running-config")

    with open("compliance/reports/cat8000v_running_config.txt", "w") as file:
        file.write(running_config)

    print("Running config saved to compliance/reports/cat8000v_running_config.txt")

    connection.disconnect()

except Exception as e:
    print("Connection failed:")
    print(e)