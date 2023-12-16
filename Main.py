import Server
import Function



run = True
DATA_SIZE = 5
number = 16
num = 0
while run:
    Server.UpdateClientList()
    for i in Server.clientList:
        if i.new:
            i.SetFunction(Function.func)
            i.new = False
    for i in Server.clientList:
        i.Start([number])
        number += DATA_SIZE
    for i in Server.clientList:
        recivedData = i.GetData()
        num += recivedData
    
    print(num)



#bytes = pickle.dumps(func)
#print(bytes)
#out = pickle.loads(bytes)
#out("23452345")

