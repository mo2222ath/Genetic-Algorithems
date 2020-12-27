class Fuzzy:

  def equ_VLowDown(x):
    return ((-x/20) + 1.5)

  def equ_lowUp(x):
    return ((x/20) - 0.5)

  def equ_lowDown(x):
    return ((-x/20) + 3)

  def equ_mediumUp(x):
    return ((x/20) - 2)
  def equ_mediumDown(x):
    return ((-x/20) + 4.5)

  def equ_highUp(x):
    return ((x/20) - 3.5)

  def equ_beginnerDown(x):
    return ((-x/15) + 2)

  def equ_intermediateUp(x):
    return ((x/15) - 1)
  def equ_intermediateDown(x):
    return ((-x/15) + 3)

  def equ_expertUp(x):
    return ((x/30) - 1)

  def getMembershipValuesForVariable1( x ):

      dictionary = {}
      
      if x >= 0 and x <= 10 : 
          dictionary['VL'] = 1
          
      if x > 10 and x < 30:
          dictionary['VL'] = Fuzzy.equ_VLowDown(x)
          dictionary['L'] = Fuzzy.equ_lowUp(x)
          
      if x >= 30 and x <= 40 :      
          dictionary['L'] = 1
          
      if x > 40 and x < 60:
          dictionary['L'] = Fuzzy.equ_lowDown(x)
          dictionary['M'] = Fuzzy.equ_mediumUp(x)
          
      if x >= 60 and x <= 70:
          dictionary['M'] = 1
          
      if x > 70 and x < 90:
          dictionary['M'] = Fuzzy.equ_mediumDown(x)
          dictionary['H'] = Fuzzy.equ_highUp(x)
      
      if x >= 90 and x <= 100:
          dictionary['H'] = 1
          
      return dictionary
  def getMembershipValuesForVariable2( x ):

      dictionary = {}
      
      if x >= 0 and x <= 15 : 
          dictionary['B'] = 1
          
      if x > 15 and x < 30:
          dictionary['B'] = Fuzzy.equ_beginnerDown(x)
          dictionary['I'] = Fuzzy.equ_intermediateUp(x)
          
      if x == 30 :      
          dictionary['I'] = 1
          
      if x > 30 and x < 45:
          dictionary['I'] = Fuzzy.equ_intermediateDown(x)
          dictionary['E'] = Fuzzy.equ_expertUp(x)
          
      if x >= 45 and x <= 60:
          dictionary['E'] = Fuzzy.equ_expertUp(x)

          
      return dictionary      
      

print(Fuzzy.equ_expertUp(20))
print(Fuzzy.getMembershipValuesForVariable1( 30))
print(Fuzzy.getMembershipValuesForVariable2( 29))