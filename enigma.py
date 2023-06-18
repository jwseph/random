# http://stanford.edu/class/archive/cs/cs106a/cs106a.1164/handouts/29-TheEnigmaMachine.pdf

A = ord('A')
N = 26

# Position AAA
III = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
II  = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
I   = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
R   = 'IXUHFEZDAOMTKQJWNSRLCYPBVG'

def idx(ch):
  return ord(ch)-A

def keep_upper(text):
  return ''.join(ch for ch in text.upper() if 0 <= idx(ch) < N)

def enc(rotor, ch):
  return rotor[idx(ch)]

def dec(rotor, ch):
  return chr(rotor.index(ch)+A)

def rotate(rotor, n):
  for _ in range(n):
    rotor = ''.join(chr((idx(ch)-1)%N+A) for ch in rotor[1:]+rotor[:1])
  return rotor

def encode(plaintext, pos='AAA'):
  plaintext = keep_upper(plaintext)
  i = rotate(I, idx(pos[0]))
  ii = rotate(II, idx(pos[1]))
  iii = rotate(III, idx(pos[2]))
  ciphertext = ''
  for ch in plaintext:
    rotate(iii, 1)
    if iii == III:
      rotate(ii, 1)
      if ii == II:
        rotate(i, 1)
    reflected = enc(R, enc(i, enc(ii, enc(iii,  ch))))
    ciphertext += dec(iii, dec(ii, dec(i, reflected)))
  return ciphertext

if __name__ == '__main__':
  print('===== THE ENIGMA MACHINE =====')
  pos = keep_upper(input('Rotor setting (ex. AAA): '))
  print('Start typing whatever text you want to encode!')
  print('TIP: The Enigma is symmetrical, so encoding is the same as decoding')
  while True:
    print(encode(input('> '), pos))