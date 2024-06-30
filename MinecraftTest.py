import subprocess
from mcrcon import MCRcon

rcon_host = "147.185.221.20"
rcon_port = 50270
rcon_password = "ikero9090"
    
structure_name = "PuestoDeExploracionImperial"
target_x = 2374
target_y = -624
target_z = 68

command = f"/npc -h"

try:
    with MCRcon(rcon_host, rcon_password, port=rcon_port) as mcr:
        mcr.command('//schem load Prueba2')
        response = mcr.command(command)
        print(response)
        
except Exception as e:
    print(f"Error: {e}")

