import subprocess
from utils import adicionar_ao_log
from funcoes_extras import list_c_directories, list_c_files

def Run_Test_Driver(folder_path, SUT_path, compiler):
    adicionar_ao_log("Running Test Driver...")
    match compiler:
        case "gcc":
            try:
                #Compila o programa C
                compile_path = list_c_directories(folder_path, SUT_path) + list_c_files(folder_path, SUT_path)
                args = ['gcc']
                args = args + (list(filter(None, compile_path))) + ["output/InstrumentedSUT/instrumented_SUT.c", "output/InstrumentedSUT/Test_Driver.c", "-o", "output/TestDriver/Test_Driver"]
                subprocess.run(args, check=True, text=True, capture_output=True) 

                # Executa o programa C
                subprocess.run(["./output/TestDriver/Test_Driver.exe"], check=True) 
            except subprocess.CalledProcessError as e:
                error = f"ERROR: TestDrive not executed properly.{e.stderr}" # {e.stderr}
                adicionar_ao_log(error)
                return error
            
        case "clang":  
            try:
                #Compila o programa C
                compile_path = list_c_directories(folder_path, SUT_path) + list_c_files(folder_path, SUT_path)
                args = ['clang']
                args = args + (list(filter(None, compile_path))) + ["output/InstrumentedSUT/instrumented_SUT.c", "output/InstrumentedSUT/Test_Driver.c", "-o", "output/TestDriver/Test_Driver"]
                subprocess.run(args, check=True, text=True, capture_output=True) 

                # Executa o programa C
                subprocess.run(["./output/TestDriver/Test_Driver.exe"], check=True)

            except subprocess.CalledProcessError as e:
                error = f"ERROR: TestDrive not executed properly.{e.stderr}" # {e.stderr}
                adicionar_ao_log(error)
                return error

    adicionar_ao_log("Test Driver executed successfully.")
    return 0


if __name__ == '__main__':

    folder_path = "tests/test_cases/case1/src"
    SUT_path = "tests/test_cases/case1/src/SUT/SUT.c"

    #Tipo de compilador
    compiler = "clang"    #gcc ou clang

    Run_Test_Driver(folder_path, SUT_path, compiler)