import re

#Split the string at every white-space character:

txt = "The rain in Spain. Your mom is ugly! Where are you going? Last time was fun."
x = re.split(r"[.!?]\s", txt)
y = len(x)
print(x)
print(y)

calc = (103*100)/21
print(calc)
