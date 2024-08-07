from mcipc.query import Client

with Client("147.185.221.21", 50598) as client:
    basic_stats = client.stats()
    full_stats = client.stats(full=True)
    
print(basic_stats)
print(full_stats)