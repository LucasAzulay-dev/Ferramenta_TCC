@echo off

set SRC_DIR=%~dp0\src
set TEST_DIR=%~dp0\test

gcc -c %SRC_DIR%\CompA\CompA.c -o %SRC_DIR%\CompA\CompA.o
gcc -c %SRC_DIR%\CompB\CompB.c -o %SRC_DIR%\CompB\CompB.o
gcc -c %SRC_DIR%\CompC\CompC.c -o %SRC_DIR%\CompC\CompC.o
gcc -c %SRC_DIR%\CompD\CompD.c -o %SRC_DIR%\CompD\CompD.o

gcc -c %SRC_DIR%\IntegrationFunction\IntegrationFunction.c -o %SRC_DIR%\IntegrationFunction\IntegrationFunction.o

gcc -DTEST_OUT -c %TEST_DIR%\Testes.c -o %TEST_DIR%\Testes.o

gcc %SRC_DIR%\CompA\CompA.o^
 %SRC_DIR%\CompB\CompB.o^
 %SRC_DIR%\CompC\CompC.o^
 %SRC_DIR%\CompD\CompD.o^
 %SRC_DIR%\IntegrationFunction\IntegrationFunction.o^
 %TEST_DIR%\Testes.o^
 -o  %TEST_DIR%\exec_tests

del /S *.o

echo Compilacao concluida com sucesso. Executando...

%TEST_DIR%\exec_tests.exe