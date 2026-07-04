def file_read(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Define the paths
sdk_py_path = r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\sdk.py'
init_py_path = r'C:\Windows\System32\OpenJarvis\src\openjarvis\agents\__init__.py'

# Read and print the contents of sdk.py
sdk_py_content = file_read(sdk_py_path)
print("Contents of sdk.py:")
print(sdk_py_content)

# Read and print the contents of __init__.py
init_py_content = file_read(init_py_path)
print("\nContents of __init__.py:")
print(init_py_content)