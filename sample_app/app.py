import os
print("Hello from Docksmith container - updated")
print("ENV:", os.environ.get("NAME"))
open("test.txt", "w").write("inside container")
