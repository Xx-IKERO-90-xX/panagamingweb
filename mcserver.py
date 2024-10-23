from mcrcon import MCRcon

host = "147.185.221.22"
port = 32422

try:
    with MCRcon(host, "ikero9090", port=port) as mcr:
        response = mcr.command("op THE_IKERO90")
        print(response)

except Exception as e:
    print(f"Error al conectarse con el RCON: {e}")