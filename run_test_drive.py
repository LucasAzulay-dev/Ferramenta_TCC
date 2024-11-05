import subprocess

def Run_Test_Driver(compiler):
    match compiler:
        case "gcc":
            #Compila o programa C
            subprocess.run(["gcc", "instrumented_SUT.c", "Test_Driver.c", "-o", "Test_Driver"], check=True)   

            # Executa o programa C
            subprocess.run([".\Test_Driver.exe"], check=True)
        
        case "clang":   #OPÇÃO NÃO TESTADA
            #Compila o programa C
            subprocess.run(["clang", "instrumented_SUT.c", "Test_Driver.c", "-o", "Test_Driver"], check=True)  

            # Executa o programa C
            subprocess.run([".\Test_Driver.exe"], check=True)


if __name__ == '__main__':
    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    Run_Test_Driver(compiler)