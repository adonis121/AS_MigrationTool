# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# main_script.ps1

$pythonExe = "python"  # or the full path to the python executable, e.g., "C:\Python39\python.exe"
$scriptPath = "my_functions.py"


$name = "Adonis"
$command = "$pythonExe $scriptPath -c 'from my_functions import greet; greet(`"$name`")'"
Invoke-Expression $command

$command = "$pythonExe $scriptPath -c 'from my_functions import farewell; farewell(`"$name`")'"
Invoke-Expression $command

