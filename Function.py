
def func(argList):
    num = argList[0]
    DATA_SIZE = 5
    val = 0
    for i in range(0,DATA_SIZE*2,2):
        addVal =  4 / (num + i)
        if (num + i / 2) % 2 == 0:
            addVal *= -1
        val += addVal
    return val

if __name__ == "__main__":
    num = 0
    number = 1
    while 1:
        num += func([number])
        number += 5
        print(num)