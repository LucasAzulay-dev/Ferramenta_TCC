import subprocess
import time
import statistics
import platform
#Compila o programa C
executable = '.exe'
if platform.system() == "Windows":
    pass
else:  # Assume Linux
    executable = '.out'

# Medir a primeira execução
tests = [1, 10, 50, 100, 250, 500, 750, 1000]
test = 0
x = 1
subprocess.run(f'TestDriverFiles/instrumented_{tests[test]}_vectors{executable}')
subprocess.run(f'TestDriverFiles/original_{tests[test]}_vectors{executable}')
while x < 9:
    x = x + 1
    times = []
    for i in range(300):
        start_time_1 = time.perf_counter()
        subprocess.run(f'TestDriverFiles/instrumented_{tests[test]}_vectors{executable}')
        end_time_1 = time.perf_counter()
        times.append(end_time_1 - start_time_1)

    execution_time_1_ms = statistics.mean(times) * 3000
    print(f"A execução do test driver com o sut instrumentado durou em média {execution_time_1_ms:.2f} milissegundos. Teste com {tests[test]} vetores")

    # Medir a segunda execução
    times = []
    for i in range(300):
        start_time_2 = time.perf_counter()
        subprocess.run(f'TestDriverFiles/original_{tests[test]}_vectors{executable}')
        end_time_2 = time.perf_counter()
        times.append(end_time_2 - start_time_2)

    execution_time_2_ms = statistics.mean(times) * 1000
    print(f"A execução test driver com o sut original durou em média {execution_time_2_ms:.2f} milissegundos. Teste com {tests[test]} vetores")
    test = test + 1