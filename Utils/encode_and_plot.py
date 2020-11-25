import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
def unipolar(sequence, pos_logic= True):
    bit = 1
    if not pos_logic:
        bit = -1
    sequence_mod = [bit if i==1 else 0 for i in sequence]
    sequence_mod.insert(0,sequence_mod[0])
    return sequence_mod

def polar_nrz_l(sequence, pos_logic = True):
    bit = 1
    if not pos_logic:
        bit = -1
    sequence_mod=[bit*(-1) if i==0 else bit for i in sequence]
    sequence_mod.insert(0,sequence_mod[0])
    return sequence_mod

def polar_nrz_i(sequence,pos_logic = True):
    bit = -1
    if not pos_logic:
        bit = 1
    sequence_mod = []
    sequence_mod.insert(0,bit)
    for i in range(len(sequence)):
        if sequence[i] == 1:
            bit = bit*(-1)
            sequence_mod.append(bit)
        else:
            sequence_mod.append(bit)
    return sequence_mod

def polar_rz(sequence,pos_logic=True):
    bit = 1
    x_axis = []
    y_axis = []
    k = 0
    if not pos_logic:
        bit = -1
    for i in sequence:
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

def Manchester(sequence,ieee_scheme=False):
    y_axis = []
    x_axis = []
    k = 0
    bit = -1
    if ieee_scheme:
        bit = 1
    for i in range(len(sequence)):
        if sequence[i] == 1:
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
    return x_axis,y_axis

def Differential_manchester(sequence,pos_logic= True):
    y_axis = []
    x_axis = []
    bit = 1
    if not pos_logic:
        bit = -1
    k = 0
    y_axis.append(bit)
    x_axis.append(k)
    for i in sequence:
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
    return x_axis,y_axis

def AMI(sequence,pos_logic=True):
    bit = 1
    sequence_mod = [0] * len(sequence)
    if not pos_logic:
        bit = -1
    sequence_mod.insert(0,sequence[0]*bit)
    for i in range(len(sequence)):
        if sequence[i] ==1:
            sequence_mod[i+1] = bit
            bit *= -1
        else:
            sequence_mod[i+1] = 0
    return sequence_mod

def check_consecutive_zeros(i,sequence,size):
    for j in range(size):
        if sequence[i+j] != 0:
            return False
    return True

def B8ZS(sequence,starting_bit_pos = True):
    sequence_mod = AMI(sequence)
    inp2 = []
    prev_bit = 1
    if not starting_bit_pos:
        prev_bit = -1
    i = 0
    while i < len(sequence):
        if sequence[i] == 1:
            prev_bit = sequence_mod[i+1]
        if i+8<=len(sequence) and check_consecutive_zeros(i,sequence,8):
            a = []
            if prev_bit ==1:
                a = [0,0,0,1,-1,0,-1,1]
            else:
                a = [0,0,0,-1,1,0,1,-1]
            for j in range(8):
                inp2.append(a[j])
            i+=8
        else:
            inp2.append(sequence_mod[i+1])
            i+=1
    inp2.insert(0,sequence_mod[0])
    return inp2

def HDB3(sequence):
    sequence_mod = AMI(sequence)
    inp2 = []
    count = 0
    prev_bit = -1
    i = 0
    while i < len(sequence):
        if sequence[i] == 1:
            count += 1
        if i+4<=len(sequence) and check_consecutive_zeros(i,sequence,4):
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
            if sequence[i] == 1:
                prev_bit *= -1
                inp2.append(prev_bit)
            else:
                inp2.append(0)
            i+=1
    inp2.insert(0,sequence_mod[0])
    return inp2

def plot_unipolar(sequence,pos=True):
    ax = plt.subplot()
    plt.ylabel("Unipolar")
    x = np.arange(len(sequence))
    logic = "Positive Logic"
    if not pos:
        logic = "Negative Logic"
    plt.xlabel(logic)
    plt.plot(unipolar(sequence,pos),color='red',drawstyle='steps-pre',linewidth=4.0)
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(x,sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_nrz_l(sequence,pos=True):
    ax = plt.subplot()
    plt.ylabel("NRZ-L")
    logic = "Positive Logic"
    if not pos:
        logic = "Negative Logic"
    plt.xlabel(logic)
    x = np.arange(len(sequence))
    plt.plot(polar_nrz_l(sequence,pos),color='red',drawstyle='steps-pre',marker='.',linewidth=4.0,markersize=18,markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(x,sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_nrz_i(sequence,pos=True):
    ax = plt.subplot()
    plt.ylabel("NRZ-I")
    logic = "Positive Logic"
    if not pos:
        logic = "Negative Logic"
    plt.xlabel(logic)
    y = polar_nrz_i(sequence,pos)
    markers = ['o' if y[i]==y[i-1] else 'x' for i in range(1,len(y))]
    x = np.arange(len(y))
    plt.plot(x,y,color='red',drawstyle='steps-pre',linewidth=2.0,markersize=18,markerfacecolor='blue')
    for i in range(len(markers)):
        plt.scatter(x[i],y[i+1],marker=markers[i])
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(x,sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_manchester(sequence,ieee=False):
    ax = plt.subplot()
    plt.ylabel("Manchester")
    logic = "G.E Thomas Logic"
    if ieee:
        logic = "IEEE Logic"
    plt.xlabel(logic)
    x,y = Manchester(sequence,ieee)
    plt.step(x,y,where='mid',marker='.',linewidth=4.0,markersize=20,color='red',markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(range(len(sequence)),sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_differential_manchester(sequence,pos = True):
    ax = plt.subplot()
    plt.ylabel("Differential Manchester")
    logic = "Negative Logic"
    if pos:
        logic = "Positive Logic"
    plt.xlabel(logic)
    x,y = Differential_manchester(sequence,pos)
    plt.step(x,y,where='mid',marker='.',linewidth=4.0,markersize=20,color='red',markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(range(len(sequence)),sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_ami(sequence,pos= True):
    ax = plt.subplot()
    plt.ylabel("AMI")
    logic = "Negative Logic"
    if pos:
        logic = "Positive Logic"
    plt.xlabel(logic)
    plt.plot(AMI(sequence,pos),color='red',drawstyle='steps-pre',marker='.',linewidth=4.0,markersize=20,markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(range(len(sequence)),sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_B8ZS(sequence,pos=True):
    ax = plt.subplot()
    plt.ylabel("B8ZS")
    logic = "Negative Logic"
    if pos:
        logic = "Positive Logic"
    plt.xlabel(logic)
    plt.plot(B8ZS(sequence,pos),color='red',drawstyle='steps-pre',marker='.',linewidth=4.0,markersize=20,markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(range(len(sequence)),sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_HDB3(sequence):
    ax = plt.subplot()
    plt.ylabel("HDB3")
    plt.plot(HDB3(sequence),color='red',drawstyle='steps-pre',marker='.',linewidth=4.0,markersize=20,markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(range(len(sequence)),sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64

def plot_rz(sequence):
    ax = plt.subplot()
    plt.ylabel("Polar RZ")
    x,y = polar_rz(sequence)
    plt.step(x,y,where='mid',marker='.',linewidth=4.0,markersize=20,color='red',markerfacecolor='blue')
    ax.grid(True,linestyle='--')
    ax.set_xticks(range(0,len(sequence)+1))
    plt.axhline(0,color='black')
    plt.axvline(0,color='black')
    for i,j in zip(range(len(sequence)),sequence):
        ax.annotate(str(j),xy=(i+0.25,0))
    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    plt.close()
    return image_base64
