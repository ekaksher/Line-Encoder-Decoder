import matplotlib.pyplot as plt
import numpy as np

def unipolar(inp, pos_logic= True):
    bit = 1
    if not pos_logic:
        bit = -1
    inp = [bit if i==1 else 0 for i in inp]
    inp.insert(0,inp[0])
    return inp

def polar_nrz_l(inp, pos_logic = True):
    bit = 1
    if not pos_logic:
        bit = -1
    inp=[bit*(-1) if i==0 else bit for i in inp]
    inp.insert(0,inp[0])
    print(inp)
    return inp

def polar_nrz_i(inp,pos_logic = True):
    bit = -1
    if not pos_logic:
        bit = 1
    inp.insert(0,bit)
    for i in range(1,len(inp)):
        if inp[i] == 1:
            bit = bit*(-1)
            inp[i] = bit
        else:
            inp[i] = bit
    print(inp)
    return inp

def polar_rz(inp,pos_logic=True):
    bit = 1
    x_axis = []
    y_axis = []
    k = 0
    if not pos_logic:
        bit = -1
    for i in inp:
        if i==0:
            y_axis.append(bit*(-1))
            x_axis.append(k)
            k+=1
            y_axis.append(0)
            x_axis.append(k)
        else:
            y_axis.append(bit)
            x_axis.append(k)
            k+=1
            y_axis.append(0)
            x_axis.append(k)
    return x_axis,y_axis

def Biphase_manchester(inp,ieee_scheme=False):
    y_axis = []
    x_axis = []
    k = 0
    bit = -1
    if ieee_scheme:
        bit = 1
    for i in range(len(inp)):
        if inp[i] == 1:
            x_axis.append(k)
            y_axis.append(-bit)
            k+=1
            y_axis.append(bit)
            x_axis.append(k)
        else:
            x_axis.append(k)
            y_axis.append(bit)
            k+=1
            y_axis.append(-bit)
            x_axis.append(k)
    print(x_axis)
    print(y_axis)
    return x_axis,y_axis

def Differential_manchester(inp,pos_logic= True):
    y_axis = []
    x_axis = []
    bit = 1
    if not pos_logic:
        bit = -1
    k = 0
    y_axis.append(bit)
    x_axis.append(k)
    for i in inp:
        if i==0:
            y_axis.append(bit* (-1))
            x_axis.append(k)
            k+=1
            y_axis.append(bit)
            x_axis.append(k)
        else:
            y_axis.append(bit)
            x_axis.append(k)
            k+=1
            bit = bit * (-1)
            y_axis.append(bit)
            x_axis.append(k)
    print(x_axis)
    print(y_axis)
    return x_axis,y_axis

def AMI(inp,pos_logic=True):
    bit = 1
    inp1 = [0] * len(inp)
    if not pos_logic:
        bit = -1
    inp1.insert(0,inp[0]*bit)
    for i in range(len(inp)):
        if inp[i] ==1:
            inp1[i+1] = bit
            bit *= -1
        else:
            inp1[i+1] = 0
    print(inp1)
    return inp1
def check_consecutive_zeros(i,inp,size):
    for j in range(size):
        if inp[i+j] != 0:
            return False
    return True
def B8ZS(inp,starting_bit_pos = True):
    inp1 = AMI(inp)
    inp2 = []
    prev_bit = 1
    if not starting_bit_pos:
        prev_bit = -1
    i = 0
    while i < len(inp):
        if inp[i] == 1:
            prev_bit = inp1[i+1]
        if i+8<=len(inp) and check_consecutive_zeros(i,inp,8):
            a = []
            if prev_bit ==1:
                a = [0,0,0,1,-1,0,-1,1]
            else:
                a = [0,0,0,-1,1,0,1,-1]
            for j in range(8):
                inp2.append(a[j])
            i+=8
        else:
            inp2.append(inp1[i+1])
            i+=1
    inp2.insert(0,inp1[0])
    print(inp1)
    print(inp2)
    return inp2
def HDB3(inp):
    inp1 = AMI(inp)
    inp2 = []
    count = 0
    prev_bit = -1
    i = 0
    while i < len(inp):
        if inp[i] == 1:
            count += 1
        if i+4<=len(inp) and check_consecutive_zeros(i,inp,4):
            a = []
            if count%2==0:
                prev_bit *= -1
                a = [prev_bit,0,0,prev_bit]
                count+=2
            else:
                a = [0,0,0,prev_bit]
                count+=1
            for j in range(4):
                inp2.append(a[j])
            i+=4
        else:
            if inp[i] == 1:
                prev_bit *= -1
                inp2.append(prev_bit)
            else:
                inp2.append(0)
            i+=1
    inp2.insert(0,inp1[0])
    return inp2
def plot(li):
    # plt.subplot(7,1,1)
    # plt.ylabel("Unipolar-NRZ")
    # plt.plot(unipolar(li,False),color='red',drawstyle='steps-pre',marker='>')
    # plt.subplot(7,1,2)
    # plt.ylabel("P-NRZ-L")
    # plt.plot(polar_nrz_l(li,False),color='blue',drawstyle='steps-pre',marker='>')
    # plt.subplot(7,1,3)
    # plt.ylabel("P-NRZ-I")
    # plt.plot(polar_nrz_i(li),color='green',drawstyle='steps-pre',marker='>')
    # plt.subplot(7,1,4)
    # plt.ylabel("Polar-RZ")
    # x,y = polar_rz(li)
    # plt.step(x,y,where='mid',marker='.')
    # x,y = Biphase_manchester(li,True)
    # plt.subplot(7,1,1)
    # plt.ylabel("Manchester")
    # plt.step(x,y,where='mid',marker='.')
    # ax = plt.subplot(7,1,1)
    # plt.ylabel("Dif_Man")
    # x,y = Differential_manchester(li,False)
    # plt.step(x,y,where='mid',marker='.')
    # ax.grid(True,linestyle='--')
    # ax.set_xticks(range(0,len(y)//2))
    # plt.subplot(7,1,7)
    # plt.ylabel("A-M-I")
    # plt.plot(AMI(li),color='blue',drawstyle='steps-pre',marker='>')
    plt.plot(B8ZS(li),color='blue',drawstyle='steps-pre',marker='>')
    # plt.plot(HDB3(li),color='blue',drawstyle='steps-pre',marker='>')
    plt.show()
                

if __name__=='__main__':
    # print("Enter the size of Encoded Data : ")
    # size=int(input())
    print('Enter the binary bits sequnce of length  bits : \n')
    li = list(map(int,list(input())))
    # print("li is ",li)
    # li = [1,0,1,0,1]
    plot(li) 