T = [0,4,6,8,11,17,18,25,0,0,0]
def P(pos, val):
  if T[pos] == 0: return
  if T[pos] >= val:
    T[pos] = T[pos+1]
  P(pos+1, val)
P(1, 11)
print T
