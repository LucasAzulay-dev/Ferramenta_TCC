import subprocess
import time
import statistics
import platform
#Compila o programa C
executable = '{executable}'
if platform.system() == "Windows":
    pass
else:  # Assume Linux
    executable = '.out'

# Medir a primeira execução
test = 1
x = 1
subprocess.run(f'TestDriverFiles/instrumented_{test}_vectors{executable}')
subprocess.run(f'TestDriverFiles/original_{test}_vectors{executable}')
while x < 5:
    x = x + 1
    times = []
    for i in range(20):
        start_time_1 = time.perf_counter()
        subprocess.run(f'TestDriverFiles/instrumented_{test}_vectors{executable}')
        end_time_1 = time.perf_counter()
        times.append(end_time_1 - start_time_1)

    execution_time_1_ms = statistics.mean(times) * 1000
    print(f"A execução do test driver com o sut instrumentado durou em média {execution_time_1_ms:.2f} milissegundos. Teste com {test} vetores")

    # Medir a segunda execução
    times = []
    for i in range(20):
        start_time_2 = time.perf_counter()
        subprocess.run(f'TestDriverFiles/original_{test}_vectors{executable}')
        end_time_2 = time.perf_counter()
        times.append(end_time_2 - start_time_2)

    execution_time_2_ms = statistics.mean(times) * 1000
    print(f"A execução test driver com o sut original durou em média {execution_time_2_ms:.2f} milissegundos. Teste com {test} vetores")
    test = test * 10