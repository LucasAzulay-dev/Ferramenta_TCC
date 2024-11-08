import subprocess
from utils import adicionar_ao_log

def Run_Test_Driver(compiler):
    adicionar_ao_log("Executando Test Driver...")
    match compiler:
        case "gcc":
            #Compila o programa C
            subprocess.run(["gcc", "output\InstrumentedSUT\instrumented_SUT.c", "output\InstrumentedSUT\Test_Driver.c", "-o", "output\TestDriver\Test_Driver"], check=True)  #-o 

            # Executa o programa C
            subprocess.run([".\output\TestDriver\Test_Driver.exe"], check=True) 
            
        
        case "clang":   #OPÇÃO NÃO TESTADA
            #Compila o programa C
            subprocess.run(["clang", "output\InstrumentedSUT\instrumented_SUT.c", "output\TestDriver\Test_Driver.c", "-o", "Test_Driver"], check=True)  

            # Executa o programa C
            subprocess.run([".\Test_Driver.exe"], check=True)
    adicionar_ao_log("Test Driver executado com sucesso.")


if __name__ == '__main__':
    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    Run_Test_Driver(compiler)