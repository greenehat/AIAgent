from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

#print(get_file_content("calculator","lorem.txt"))
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))


