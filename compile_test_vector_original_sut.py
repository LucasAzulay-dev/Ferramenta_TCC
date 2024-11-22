import subprocess
import platform
#Compila o programa C
executable = '.exe'
if platform.system() == "Windows":
    pass
else:  # Assume Linux
    executable = '.out'
tests = [1, 10, 50, 100, 250, 500, 750, 1000]
test = 0
while test <= 7:
    args = ['gcc']
    args = args + (list(['TestDriversSource/sut.c', f'TestDriversSource/Test_Driver_sut_original_{tests[test]}.c', "-o", f"TestDriverFiles/original_{tests[test]}_vectors{executable}"]))
    subprocess.run(args, check=True, text=True, capture_output=True) 

    args = ['gcc']
    args = args + (list(['TestDriversSource/instrumented_SUT.c', f'TestDriversSource/Test_Driver_sut_instrumented_{tests[test]}.c', "-o", f"TestDriverFiles/instrumented_{tests[test]}_vectors{executable}"]))
    subprocess.run(args, check=True, text=True, capture_output=True) 
    test = test + 1