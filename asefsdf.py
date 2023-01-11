import numpy as np
import pandas as pd  

a = []
b = ['asdf','asdf']
c = ['safd','safd']

ad = pd.DataFrame()

a.append(b)
a.append(c)
print(a)

a = pd.DataFrame(a)

print(pd.concat([a,ad]))

