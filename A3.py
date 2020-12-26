
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


print(Fuzzy.equ_expertUp(20))