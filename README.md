# DC/CC Coupling Analysis Tool

This is the final delivery of the Embedded Software for the Aeronautical Industry Specialization, offered by Embraer in partnership with UFPE. 

This work proposes a tool for automating the execution of test cases and the measurement of data and control coupling coverage on a SUT written in ANSI C for aeronautical applications. The tool uses static code instrumentation techniques to gather information about the code execution during the test cases, facilitating a white-box approach to code verification. The tool generates a report that presents the information relevant to data and control coupling analysis.

## How to Use

### Requirements

This project was developed and tested for Windows. First, the latest version of **python 3** and **pip** is needed. A C code compiler is also required, it should be **gcc** or **clang**. In order to generate the code diagram, the latest verion of **graphviz** should be installed.

To install the required python packages, execute the comannd in the project root folder:

```pip install -r requirements.txt```

### Graphical Interface

In order to initiate the tool, execute the .bat file:

```bat_scripts\run_dc_cc_tool.bat```

or run the python command:

```python src\graphical_interface.py```

The tool's graphical interface will initiate. Inform the required inputs and click 'Run tool'. The report will be presented in the interface. Use the buttons below the report to navigate through the pages and other files.

## Execute test cases

There are some prepared test cases in the project. You can check them in the _tests\test_cases_ file. Test cases can be executed individually thought the graphical interface or, to run all the tests, execute:

```bat_scripts\run_tests.bat```

This will save all the outputs in the _output_ folder of each test case. Some test cases will not produce outputs if the intended behaviour is to raise some error.
