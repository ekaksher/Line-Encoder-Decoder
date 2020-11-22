#Generating Random Bits
import random
SIZE = int(input("Enter the number of bits required \n"))
bits = ["0","1"]
sequence = []
zeros=0
count = 0
while(True):
    zeros = int(input("Enter how many consecutive zeros are need! Else Enter 0 \n"))
    if zeros > 0:
        count = int(input("Enter frequency of consecutive zeros in the bit \n"))
    if ((zeros * count)>SIZE):
        print("Number of required consecutive Zeros exceed given number of bits. Try Again")
    else:
        break
if zeros> 0:
    for i in range(count):
        sequence.append("0"*zeros)
for i in range(SIZE-(zeros*count)):
    sequence.append(random.choice(bits))
#Shuffling The Bits To Make Consecutive Zeros Random
random.shuffle(sequence)
#Mapping The Numbers back to int
sequence = list(map(int,list("".join(sequence))))
#Getting Longest Palindromic SubString
def get_modified_string(sequence):
    i = 0
    modified_sequence = ["#"]
    while(i<len(sequence)):
        modified_sequence.append(sequence[i])
        modified_sequence.append("#")
        i +=1
    return modified_sequence
def manachers_algorithm(sequence):
    sequence = get_modified_string(sequence)
    size = len(sequence)
    lps = [0] * size
    c = 0
    r = 0
    maxlen = 0
    index = 0
    for i in range(size):
        mirror = (2*c) - i
        if(i<r):
            lps[i] = min(r-i,lps[mirror])
        a = i + (1+lps[i])
        b = i - (1+ lps[i])
        while(a <size and b>=0 and sequence[a]==sequence[b]):
            lps[i] += 1
            a +=1
            b -=1
        if (i + lps[i] > r):
            c = i
            r = i + lps[i]
            if(lps[i]>maxlen):
                maxlen = lps[i]
                index = i
    return maxlen,index,sequence
maxlen,index,sequence_mod = manachers_algorithm(sequence)
palindrome = sequence_mod[index-maxlen:index+maxlen+1]
palindrome = [i for i in palindrome if i != '#']
print(f"Longest Palindrom in {sequence} is {palindrome} of size {len(palindrome)}")