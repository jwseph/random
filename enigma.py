# http://stanford.edu/class/archive/cs/cs106a/cs106a.1164/handouts/29-TheEnigmaMachine.pdf

def enc(rotor, ch):
  return rotor[ord(ch)-ord('A')]

def dec(rotor, ch):
  return chr(rotor.index(ch)+ord('A'))

I   = 'JGDQOXUSCAMIFRVTPNEWKBLZYH'
II  = 'NTZPSFBOKMWRCJDIVLAEYUXHGQ'
III = 'JVIUBHTCDYAKEQZPOSGXNRMWFL'
UKW = 'QYHOGNECVPUZTFDJAXWMKISRBL'
ETW = 'QWERTZUIOASDFGHJKPYXCVBNML'


# pos A
III = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
II  = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
I   = 

def rotate(rotor):
  return ''.join(chr((ord(ch)-ord('A')-1)%26+ord('A')) for ch in rotor[1:]+rotor[:1])

print(III)
for _ in range(25):
  III = rotate(III)
print(III)
print(rotate(III))

def encode(plaintext, pos='AAA'):
  pI, pII, pIII = pos
  ciphertext = ''
  for ch in plaintext:
    ciphertext += dec(III, dec(II, dec(I, enc(ETW, enc(I, enc(II, enc(III, ch)))))))
  return ciphertext

def decode(plaintext, pos='AAA'):
  pI, pII, pIII = pos
  ciphertext = ''
  for ch in plaintext:
    ciphertext += dec(III, dec(II, dec(I, dec(ETW, enc(I, enc(II, enc(III, ch)))))))
  return ciphertext

text = 'HELLOWORLD'
print(text)
print(''.join(enc(I, ch) for ch in text))
print(''.join(dec(I, enc(I, ch)) for ch in text))
print(encode('HELLOWORLD'))
print(decode(encode('HELLOWORLD')))