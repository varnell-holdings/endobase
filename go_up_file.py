import os.path
add = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(add)
print(add)
print(base)
new_path = os.path.join(base, "endobase_local")
print(new_path)
