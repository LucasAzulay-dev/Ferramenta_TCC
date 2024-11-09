import subprocess

def Run_Test_Driver(compiler):
    match compiler:
        case "gcc":
            #Compila o programa C
            subprocess.run(["gcc", "output/InstrumentSUT/instrumented_SUT.c", "output/InstrumentSUT/Test_Driver.c", "-o", "output/TestDriver/Test_Driver"], check=True)  #-o 

            # Executa o programa C
            subprocess.run(["./output/TestDriver/Test_Driver.exe"], check=True) 
            
        
        case "clang":   #OPÇÃO NÃO TESTADA
            #Compila o programa C
            subprocess.run(["clang", "output/InstrumentSUT/instrumented_SUT.c", "output/TestDriver/Test_Driver.c", "-o", "output/TestDriver/Test_Driver"], check=True)  

            # Executa o programa C
            subprocess.run(["./output/TestDriver/Test_Driver.exe"], check=True) 


if __name__ == '__main__':
    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    Run_Test_Driver(compiler)