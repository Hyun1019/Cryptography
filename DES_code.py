#-*- coding:utf-8 -*-

IP = [58,50,42,34,26,18,10,2,        #초기벡터
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

FP = [40,8,48,16,56,24,64,32,        #초기벡터 역함수 = final 벡터
      39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30,
      37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28,
      35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26,
      33,1,41,9,49,17,57,25]

EP = [32,1,2,3,4,5,                  #Expand p-box (R 32bit를 48bit로)
      4,5,6,7,8,9,
      8,9,10,11,12,13,
      12,13,14,15,16,17,
      16,17,18,19,20,21,
      20,21,22,23,24,25,
      24,25,26,27,28,29,
      28,29,30,31,32,1]

PC1 = [57,49,41,33,25,17,9,63,55,47,39,31,23,15,
       1,58,50,42,34,26,18,7,62,54,46,38,30,22,
       10,2,59,51,43,35,27,14,6,61,53,45,37,29,
       19,11,3,60,52,44,36,21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

shift_n = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]   #subkey 생성 시, 1 2 9 16 때만 1번 shift rotate
     
S_box = [[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
          [0,15,7,4,14,2,13,10,3,6,12,11,9,5,3,8],
          [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
          [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
         [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
          [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
          [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
          [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
         [[10,0,9,14,6,3,15,5,1,14,12,7,11,4,2,8],
          [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
          [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
          [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
         [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
          [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
          [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
          [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
         [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
          [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
          [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
          [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
         [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
          [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
          [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
          [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
         [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
          [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
          [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
          [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
         [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
          [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
          [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
          [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]]

P_box = [16,7,20,21,29,12,28,17,              #straight p-box 
         1,15,23,26,5,18,31,10,
         2,8,24,14,32,27,3,9,
         19,13,30,6,22,11,4,25] 


import random  


def getPlaintext(plain):                  #input data를 바이너리로 변환하는 함수.
    pad = 'A'                             #padding 문자는 임의로 'A'로 지정.
    if len(plain) % 8 != 0:               
        for i in range(7):            
            plain += pad                   
            if (len(plain) % 8 == 0):
                break
            
    plaintext = []
    for i in range(len(plain)):           #한 문자씩 ASCII 값으로 변환 후, 바이너리로 출력.
        plaintext.append(bin(ord(plain[i]))[2:].zfill(8))
    return ''.join(plaintext)
        

def getCiphertext(cipher):                #바이너리로 된 암호문을 문자화하는 함수.
    result = ''
    for i in range(8):                   
        result += chr(int(cipher[8*i:8*(i+1)], 2))
    return result


def Permutation(mid, table):                #순열함수. 
    n = len(table)
    result = ''
    for i in range(n):
        result += mid[table[i]-1]
    return result

    
def left_rotate(mid_key, n):                 #subkey 생성 시 거치는 left rotate 함수.          
    return mid_key[n:] + mid_key[:n]

class DES:
    
    encrypt_key = ''                         #복호화 key를 위한 클래스 변수. 
    encrypt_res = ''                         #복호화를 위해 Encrypt 결과를 저장하는 클래스 변수.
        
    def subKey(mid_key, n):                  #subkey 생성 함수.
        length = int(len(mid_key) / 2)       #56bit의 key를 반으로 나눠 해당 round수에 맞게 각각 shift rotate.
        key = left_rotate(mid_key[:length], n) + left_rotate(mid_key[length:], n)
        return Permutation(key, PC2)         #shift rotate 후, PC2 table로 축소 순열.


    def s_box(RK_xor):                       #s-box 함수. 48bit (8 x 6bit)를 32bit (8 x 4bit)로 치환.
        result = ''
        for i in range(8):                  
            mid_xor = RK_xor[6*i:6*(i+1)]    
            b = int(mid_xor[1:5], 2)         #6bit의 가운데 4bit로 S_box[i][a][b] 중, b 지정. 
            if mid_xor[0] == mid_xor[-1]:    #6bit의 앞뒤 2bit를 비교하는 조건문으로 a 지정.
                if (mid_xor[0] == 0): a = 0
                else: a = 3
            else:
                if (mid_xor[0] == 0): a = 1
                else: a = 2
            result += bin(S_box[i][a][b])[2:].zfill(4)   
        return result    
    
    
    def f_box(L, R, key, shift_list):        #f_box 함수.
        for i in range(16):
            exp_R = Permutation(R, EP)       #R 32bit를 EP를 통해 48bit로 확장.
            subkey = DES.subKey(key, shift_list[i])   #56bit의 key로 48bit의 subkey 생성.

            RK_xor = bin(int(exp_R, 2) ^ int(subkey, 2))[2:].zfill(48) #확장된 R과 subkey를 XOR.
            SP_box_res = Permutation(DES.s_box(RK_xor), P_box)         #XOR한 값을 S_box 치환 후, P_box 순열. 
            final_xor = bin(int(SP_box_res, 2) ^ int(L, 2))[2:].zfill(32) #f-함수 결과를 L과 XOR.
       
            if i == 15:                      #마지막 round는 swap 일어나지 않으므로.
                L = final_xor
                DES.encrypt_key = key        #복호화 과정을 위해 마지막 라운드에서 쓰인 key를 저장.
            else:
                L = R
                R = final_xor  
        return L + R
    
    
    def Encrypt(input_data):
        plain = getPlaintext(input_data)
        n = int(len(plain) / 64)
        mid_plain = []; plaintext = []; cipher = ''; DES.encrypt_res = ''
        
        mid_key = format(random.getrandbits(64), 'b').zfill(64)  
        for i in range(n):
            mid_plain.append(plain[64*i:64*(i+1)])               
            plaintext.append(Permutation(mid_plain[i], IP))      
            L = plaintext[i][:32]                                 
            R = plaintext[i][32:]
        
            key = Permutation(mid_key, PC1)                       #PC1으로 64bit key를 56bit key로 축소.
            result = Permutation(DES.f_box(L, R, key, shift_n), FP) #f_box 호출 후, 최종 순열.
            DES.encrypt_res += result                             #용이한 복호화를 위해 암호문 (바이너리) 저장. 
            cipher += getCiphertext(result)                     
        return cipher
    
    
    def Decrypt(output_data):
        cipher = DES.encrypt_res                          #Encrypt 결과 (바이너리)를 복호화.
        mid_cipher = []; ciphertext = []; shift_d = []; re_plain = ''
        n = int(len(cipher) / 64)
        
        for i in range(1, 17):                            #암호화 때 쓰인 key가 역순으로 들어가므로.
            shift_d.append(shift_n[-i])
        
        for i in range(n):
            mid_cipher.append(cipher[64*i:64*(i+1)])
            ciphertext.append(Permutation(mid_cipher[i], IP))
            L = ciphertext[i][:32]
            R = ciphertext[i][32:]
            
            result = Permutation(DES.f_box(L, R, DES.encrypt_key, shift_d), FP)
            re_plain += getCiphertext(result) 
        return re_plain
    
        
with open("input.txt", 'r') as f:
    input_data = f.read()

print('<평문>')
print(input_data)

print('\n<암호문>')
output_data = DES.Encrypt(input_data)
print(output_data)

print('\n<복호문>')
decrypt_data = DES.Decrypt(output_data)
print(decrypt_data)

with open("output.txt", 'w') as f:
    f.write(decrypt_data)         
    
    

   

            
