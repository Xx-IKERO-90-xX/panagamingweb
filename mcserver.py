from mcrcon import MCRcon

host = "192.168.1.66"
port = 25575

try:
    with MCRcon(host, "ikero9090", port=port) as mcr:
        response = mcr.command("list")
        print("Respuesta del servidor:", response)

except Exception as e:
    print(f"Error al conectarse con el RCON: {e}")