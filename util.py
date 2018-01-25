def f(n):
 c = 0
 for line in open("file.xml", encoding="utf8"):
  if (c > n):
   break
  print(line, end="")
  c += 1


def w(n):
 c = 0
 fl = open("sample.xml", "w", encoding="utf8")
 for line in open("file.xml", encoding="utf8"):
  if (c > n):
   break
  fl.write(line)
  c += 1

