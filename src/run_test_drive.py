import subprocess
from utils import adicionar_ao_log
from funcoes_extras import list_c_files

def Run_Test_Driver(folder_path, SUT_path, compiler):
    adicionar_ao_log("Running Test Driver...")
    match compiler:
        case "gcc":
            try:
                #Compila o programa C
                compile_path = list_c_files(folder_path, SUT_path)
                subprocess.run(["gcc", compile_path, "output/InstrumentedSUT/instrumented_SUT.c", "output/InstrumentedSUT/Test_Driver.c", "-o", "output/TestDriver/Test_Driver"], check=True, text=True, capture_output=True) 

                # Executa o programa C
                subprocess.run(["./output/TestDriver/Test_Driver.exe"], check=True) 
            except subprocess.CalledProcessError as e:
                error = f"ERROR: TestDrive não executado corretamente.{e.stderr}" # {e.stderr}
                adicionar_ao_log(error)
                return error
            
        
        case "clang":   #OPÇÃO NÃO TESTADA
            #Compila o programa C
            subprocess.run(["clang", "output/InstrumentedSUT/instrumented_SUT.c", "output/TestDriver/Test_Driver.c", "-o", "Test_Driver"], check=True)  

            # Executa o programa C
            subprocess.run(["./Test_Driver.exe"], check=True)

    adicionar_ao_log("Test Driver executed successfully.")
    return 0


if __name__ == '__main__':

    folder_path = "tests/test_cases/case1/SUT"
    SUT_path = "tests/test_cases/case1/SUT/SUT.c"

    #Tipo de compilador
    compiler = "gcc"    #gcc ou clang

    Run_Test_Driver(folder_path, SUT_path, compiler)