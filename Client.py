import Network
import Instructions
import pickle
import traceback

IP = Network.SelfIp()
PORT = Network.PORT
soc = Network.Client(IP, PORT)

func = None
dataBuffer = None

def Start():
    global dataBuffer
    print("Starting")
    argList = []
    argCount = soc.recive(int)    
    for i in range(argCount):
        argList.append(pickle.loads(soc.recive()))
    try:
        result = func(argList)
    except Exception as e:
        result = Instructions.ERROR + "| "  + traceback.format_exc()
    print("Sending results")
    soc.send(Instructions.GOT_DATA)
    dataBuffer = result
def SetFunction():
    global func
    functionName = soc.recive(str)
    functionSourceCode = soc.recive(str)
    print(functionSourceCode)
    namespace = {}
    exec(functionSourceCode, namespace)
    func = namespace[functionName]
def GetData():
    soc.send(pickle.dumps(dataBuffer))
def ExecInstruction():
    instruction = soc.recive(str)
    if instruction == Instructions.SEND_FUNCTION:
        SetFunction()
    elif instruction == Instructions.START:
        Start()
    elif instruction == Instructions.GET_DATA:
        GetData()
    else:
        raise Exception("Failed invlaid insturciton -> " + instruction)

while 1:
    ExecInstruction()
