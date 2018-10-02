import cx_Freeze

executables = [cx_Freeze.Executable("Gui.py",
                                    base="Win32GUI",
                                    icon=None)]

build_exe_options = {"packages": ["sys", "os", "re", 
                                  "PyQt5.QtWidgets", 
                                  "numpy",
                                  "pandas", 
                                  "mago_max", "mago_max"],
                     "include_files": []}

cx_Freeze.setup(
    name="Mago",
    version="1.0",
    description="Multi Dynamics Algorithm for Global Optimization",
    options={"build_exe": build_exe_options},
    executables=executables
)
