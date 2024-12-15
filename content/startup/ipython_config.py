c = get_config()
c.InteractiveShellApp.exec_lines = [
    'from IPython.core.magic import register_cell_magic',
    'exec(open("startup/00-hcs-processor.py").read())'
]
