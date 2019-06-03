if __name__ == '__main__':
  
  data = open("ncpus.txt") #opens pdb file in read mode

  line = data.readlines()



  m = 0


  for i in line:

      n = int(i[32])
   #make an integer of character 32 of the line
      m = m + n

  print("Number of available CPU cores: ", 48 - m)
