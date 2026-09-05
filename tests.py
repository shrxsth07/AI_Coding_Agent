from Functions.get_files_info import get_files_info
from Functions.get_file_content import get_file_content
from Functions.write_file import write_file
from Functions.run_python_file import run_python_file

def main():
    working_dir = "calculator"
    # root_contents = get_files_info(working_dir)
    # print(root_contents)
    # pkg_contents = get_files_info(working_dir, "pkg")
    # print(pkg_contents)
    # pkg_contents = get_files_info(working_dir, "/bin")
    # print(pkg_contents)
    # pkg_contents = get_files_info(working_dir, "../")
    # print(pkg_contents)

    # print(get_file_content(working_dir, "main.py"))
    # print(get_file_content(working_dir, "pkg/calculator.py"))
    # print(get_file_content(working_dir, "/bin/cat"))\

    # print(write_file(working_dir, "pkg/morelorem.txt", "testing to create a new file"))

    print(run_python_file(working_dir, "main.py", ["3 * 5"]))
    # print(run_python_file(working_dir, "tests.py"))
    # print(run_python_file(working_dir, "../main.py"))
    # print(run_python_file(working_dir, "nonexistent.py"))


main()