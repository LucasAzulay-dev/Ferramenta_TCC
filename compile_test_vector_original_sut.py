import subprocess
import platform
#Compila o programa C
executable = '.exe'
if platform.system() == "Windows":
    pass
else:  # Assume Linux
    executable = '.out'
test = 1
while test <= 1000:
    args = ['gcc']
    args = args + (list(['TestDriversSource/sut.c', f'TestDriversSource/Test_Driver_sut_original_{test}.c', "-o", f"TestDriverFiles/original_{test}_vectors{executable}"]))
    subprocess.run(args, check=True, text=True, capture_output=True) 

    args = ['gcc']
    args = args + (list(['TestDriversSource/instrumented_SUT.c', f'TestDriversSource/Test_Driver_sut_instrumented_{test}.c', "-o", f"TestDriverFiles/instrumented_{test}_vectors{executable}"]))
    subprocess.run(args, check=True, text=True, capture_output=True) 
    test = test * 10