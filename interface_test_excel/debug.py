ab={"yun":"feng"}

c={"name":"ba"}

print(c['name'])
d=c['name']

print(locals()[c['name']])
print(globals()[d])