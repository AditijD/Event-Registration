import runpy
from playsound import playsound

while True:
   try:
        file_globals = runpy.run_path("Sheetster.py")
   except Exception as e:
        print ("Exception occured: ", e)
        playsound("C:\\Users\\adi_d\\Documents\\RegDesk\\Kalesh.mp3")
