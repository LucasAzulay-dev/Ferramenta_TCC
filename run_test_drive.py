import subprocess

def Run_Test_Driver(compiler):
    match compiler:
        case "gcc":
            #Compila o programa C
            subprocess.run(["gcc", "SUT.c", "Test_Driver.c", "-o", "Test_Driver"], check=True)   #Substituir por instrumented_SUT.c

            # Executa o programa C
            subprocess.run([".\Test_Driver.exe"], check=True)
        
        case "clang":   #OPÇÃO NÃO TESTADA
            #Compila o programa C
            subprocess.run(["clang", "SUT.c", "Test_Driver.c", "-o", "Test_Driver"], check=True)   #Substituir por instrumented_SUT.c

            # Executa o programa C
            subprocess.run([".\Test_Driver.exe"], check=True)


if __name__ == '__main__':
    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    Run_Test_Driver(compiler)