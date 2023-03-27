data = "0;0;0"
print(data.split(";"))
splitData = data.split(";")
final = []
for i in splitData:
    final.append(float(i))
print(final)