import base64
import hashlib
import codecs
from Crypto.Cipher import AES

def Recover(PassNum):
    c = [7,3,1]
    temp = 0
    for i in range(21,27):
        temp += (int(PassNum[i])*c[(i-21)%3])
    temp %= 10
    return temp

def GenSeed(PassNum):
    string = ""
    ReNum = Recover(PassNum)
    string += PassNum[0:8] + "<" + PassNum[9] + PassNum[13:20] + PassNum[21:27] +str(ReNum)
    print(string)
    seed = hashlib.sha1(string.encode("utf-8")).hexdigest()[0:32]
    print(f"{seed}")
    c1 = '00000001'
    D = seed + c1
    H = hashlib.sha1(codecs.decode(D,"hex")).hexdigest()
    ka = H[0:16]
    kb = H[16:32]

    return ka,kb

def ParityCheck(k):
    key = bin(int(k,16))[2:]
    temp = 0
    res = ""
    for i in range(0,len(key)):
        if (i % 8 != 7):
            if (int(key[i]) % 2 == 1):
                temp += 1
            res = res + key[i]
        else: 
            if temp % 2 == 1:
                res = res + "0"
            else :
                res = res + "1"
            temp = 0
    return hex(int(res,2))[2:]
    


if __name__ == '__main__':
    a = "9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI"
    PassNum = "12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4"
    ka,kb = GenSeed(PassNum)
    ParityCheck(ka)
    print(ka)
    print(kb)
    key = ParityCheck(ka+kb)
    print(key)
    aes = AES.new(codecs.decode(key,'hex'),AES.MODE_CBC,iv=b'\x00'*16)
    print(aes.decrypt(codecs.decode(a.encode(),'base64')))

