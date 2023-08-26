import os, sys, random

def shred(file: str):
  size = os.path.getsize(file)
  with open(file, 'wb') as f:
    f.write(random.randbytes(size))

def main():
  files = sys.argv[1:]

  if not files:
    print('Drag and drop a file to continue')
    return

  code = str(random.randint(1, 100))
  print('Selected files:')
  print('\n'.join(f'  "{file}"' for file in files))
  if input(f'Enter {code} to confirm shredding: ').strip() != code:
    print('Canceled')
    return

  for file in files:
    shred(file)
    
if __name__ == '__main__':
  main()