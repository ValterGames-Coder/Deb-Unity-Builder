import os
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showinfo

# region Create window
window = tk.Tk()
window.title('Deb Unity Builder')
window.geometry('450x400')
window.minsize(450, 400)

s = ttk.Style()
s.configure('TNotebook.Tab', width=window.winfo_screenwidth(), font=25, padding=(20, 0), borderwidth=0)
# endregion

# region Classes
class Package:
    def __init__(self):
        self.name = ''
        self.path_to_game = ''
        self.path_to_x86_64 = ''
        self.path_to_icon = ''

    def clear(self):
        self.name = ''
        self.path_to_game = ''
        self.path_to_x86_64 = ''
        self.path_to_icon = ''


class Control:
    def __init__(self):
        self.version = ''
        self.description = ''
        self.maintainer = ''

    def clear(self):
        self.version = ''
        self.description = ''
        self.maintainer = ''


class Desktop:
    def __init__(self):
        self.name = ''
        self.comment = ''

    def clear(self):
        self.name = ''
        self.comment = ''


class BuildSetting:
    def __init__(self):
        self.package = False
        self.control = False
        self.desktop = False
        self.ready = False

    def clear(self):
        self.package = False
        self.control = False
        self.desktop = False
        self.ready = False


package = Package()
control = Control()
desktop = Desktop()
build_setting = BuildSetting()
# endregion

# region Variables
pkg_name = tk.StringVar()
dictionary = tk.StringVar()
x86_64 = tk.StringVar()
icon = tk.StringVar()
build_progress = tk.StringVar()
# endregion

# region Functions
def create_package():
    if len(pkg_name.get()) > 0:
        package.name = pkg_name.get()

        os.system(f"mkdir -p {package.name}/DEBIAN")
        os.system(f"mkdir -p {package.name}/opt/{package.name}/bin")
        os.system(f"mkdir -p {package.name}/opt/{package.name}/lib")
        os.system(f"mkdir -p {package.name}/opt/{package.name}/share/icon")
        os.system(f"mkdir -p {package.name}/"
                  f"{os.getcwd().split('/')[1] + '/' + os.getcwd().split('/')[2]}"
                  f"/.local/share/applications")

        main_frame.pack_forget()
        notebook.add(frame_package, text='Package')
        notebook.add(frame_control, text='Control')
        notebook.add(frame_desktop, text='Desktop')
        notebook.add(frame_build, text='Build')
        notebook.pack(expand=True, fill=tk.BOTH)
    else:
        showerror('Error', 'Fill in all the fields')


def set_path_to_game():
    package.path_to_game = fd.askdirectory()
    dictionary.set(package.path_to_game)
    os.system(f"cp -r {package.path_to_game}/* {package.name}/opt/{package.name}/lib")


def set_path_to_main():
    package.path_to_x86_64 = fd.askopenfilename(filetypes=[("x86_64 files", ".x86_64"), ("all", ".*")])
    x86_64.set(package.path_to_x86_64)


def set_path_to_icon():
    package.path_to_icon = fd.askopenfilename(filetypes=[("image", ".png")])
    os.system(f"cp {package.path_to_icon} {package.name}/opt/{package.name}/share/icon")
    icon.set(package.path_to_icon)


def set_path_to_build():
    build_setting.path = fd.askdirectory()


def open_doc():
    webbrowser.open('https://github.com/ValterGames-Coder/Deb-Unity-Builder#readme')


def save_package():
    if len(path_to_main_label['text']) > 0 and len(path_to_game_label['text']) > 0 and len(path_to_icon_label['text']) > 0:
        build_setting.package = True
        check_ready()
        notebook.select(1)
    else:
        showerror('Error', 'Fill in all the fields')


def save_control():
    control.version = control_version_entry.get()
    control.description = control_description_entry.get(1.0, tk.END)
    control.maintainer = control_maintainer_entry.get()

    if len(control.version) > 0 and len(control.description) > 0 and len(control.maintainer) > 0:
        os.system(f"touch {package.name}/DEBIAN/control")
        control_file = open(f'{package.name}/DEBIAN/control', 'w')
        control_file.write(
            f'Package:        {package.name}\n'
            f'Version:        {control.version}\n'
            f'Section:        game\n'
            f'Priority:       optional\n'
            f'Architecture:   amd64\n'
            f'Maintainer:     {control.maintainer}\n'
            f'Description:    {control.description}\n')
        control_file.close()
        build_setting.control = True
        check_ready()
        notebook.select(2)
    else:
        showerror('Error', 'Fill in all the fields')


def save_desktop():
    desktop.name = desktop_name_entry.get()
    desktop.comment = desktop_comment_entry.get(1.0, tk.END)

    if len(desktop.name) > 0 and len(desktop.comment) > 0:
        os.system(
            f"touch {package.name}/{os.getcwd().split('/')[1] + '/' + os.getcwd().split('/')[2]}/.local/share/applications/{package.name}.desktop")
        desktop_file = open(
            f'{package.name}/{os.getcwd().split("/")[1] + "/" + os.getcwd().split("/")[2]}/.local/share/applications/{package.name}.desktop',
            'w')
        desktop_file.write(f'[Desktop Entry]\n'
                           f'Type=Application\n'
                           f'Name={desktop.name}\n'
                           f'Comment={desktop.comment}\n'
                           f'Exec=/opt/{package.name}/bin/{package.name}-launcher\n'
                           f'Terminal=false\n'
                           f'Categories=Games\n'
                           f'Icon=/opt/{package.name}/share/icon/{package.path_to_icon.split("/")[-1]}\n')
        desktop_file.close()
        build_setting.desktop = True
        check_ready()
        notebook.select(3)
    else:
        showerror('Error', 'Fill in all the fields')


def check_ready():
    if build_setting.package is True:
        if build_setting.control is True:
            if build_setting.desktop is True:
                build_setting.ready = True


def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(build_label['text'])

def build():
    os.system(f"touch {package.name}/opt/{package.name}/bin/{package.name}-launcher")
    launcher = open(f'{package.name}/opt/{package.name}/bin/{package.name}-launcher', 'w')
    launcher.write(f'#! /bin/sh\n'
                   f'exec /opt/{package.name}/lib/{package.path_to_x86_64.split("/")[-1]}')
    launcher.close()
    os.system(f"chmod +x {package.name}/opt/{package.name}/bin/{package.name}-launcher")

    if build_setting.ready is True:
        os.system(f'dpkg-deb -b {package.name}')
        showinfo('Ready', 'Game the builded')
        build_progress.set(f'cd {os.getcwd()}\n'
                           f'dpkg -i ./{package.name}.deb')

        btn = ttk.Button(frame_build, text='Copy', command=copy_to_clipboard)
        btn.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
    else:
        showerror('Error', 'Fill in all the windows')


def new_package():
    notebook.pack_forget()
    main_frame.pack(expand=True, fill=tk.BOTH)
    package.clear()
    control.clear()
    desktop.clear()
    build_setting.clear()

# endregion

# region Notebook
notebook = ttk.Notebook()
# endregion

# region Menu
main_menu = tk.Menu()
main_menu.add_cascade(label="New Package", command=new_package)
main_menu.add_cascade(label="Help", command=open_doc)

window.config(menu=main_menu)
# endregion

# region Main label
main_label = ttk.Label(text='Deb Unity Builder', font=('Arial', 20, 'bold'),
                       padding=(6, 2))
main_label.pack(anchor=tk.N)
# endregion

# region Frames
main_frame = ttk.Frame(window)
main_frame.pack(expand=True, fill=tk.BOTH)
frame_package = ttk.Frame(notebook, width=400, height=380)
frame_control = ttk.Frame(notebook, width=400, height=380)
frame_desktop = ttk.Frame(notebook, width=400, height=380)
frame_build = ttk.Frame(notebook, width=400, height=380)
# endregion

# region Create
name_label = ttk.Label(main_frame, text="Package name: ")
name_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
package_name_entry = ttk.Entry(main_frame, font=40, textvariable=pkg_name)
package_name_entry.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
create_button = ttk.Button(main_frame, text='Create', command=create_package)
create_button.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
# endregion

# region Package
path_to_game_button = ttk.Button(frame_package, text='Game Dictionary', command=set_path_to_game)
path_to_game_button.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
path_to_game_label = ttk.Label(frame_package, textvariable=dictionary)
path_to_game_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

path_to_main_button = ttk.Button(frame_package, text='x86_64 file', command=set_path_to_main)
path_to_main_button.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
path_to_main_label = ttk.Label(frame_package, textvariable=x86_64)
path_to_main_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

path_to_icon_button = ttk.Button(frame_package, text='Icon', command=set_path_to_icon)
path_to_icon_button.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
path_to_icon_label = ttk.Label(frame_package, textvariable=icon)
path_to_icon_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

save_package_button = ttk.Button(frame_package, text='Save', command=save_package)
save_package_button.pack(anchor=tk.S, side='bottom', padx=10, pady=5, fill=tk.X)
# endregion

# region Control
control_version_label = ttk.Label(frame_control, text="Version: ")
control_version_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
control_version_entry = ttk.Entry(frame_control, width=80, font=40)
control_version_entry.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

control_description_label = ttk.Label(frame_control, text="Description: ")
control_description_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
control_description_entry = tk.Text(frame_control, width=80, height=5, font=40)
control_description_entry.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

control_maintainer_label = ttk.Label(frame_control, text="Maintainer: ")
control_maintainer_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
control_maintainer_entry = ttk.Entry(frame_control, width=80, font=40)
control_maintainer_entry.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

save_control_button = ttk.Button(frame_control, text='Save', command=save_control)
save_control_button.pack(anchor=tk.S, side='bottom', padx=10, pady=5, fill=tk.X)
# endregion

# region Desktop
desktop_name_label = ttk.Label(frame_desktop, text="Name: ")
desktop_name_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
desktop_name_entry = ttk.Entry(frame_desktop, width=80, font=40)
desktop_name_entry.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

desktop_comment_label = ttk.Label(frame_desktop, text="Comment: ")
desktop_comment_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
desktop_comment_entry = tk.Text(frame_desktop, width=80, height=5, font=40)
desktop_comment_entry.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

save_desktop_button = ttk.Button(frame_desktop, text='Save', command=save_desktop)
save_desktop_button.pack(anchor=tk.S, side='bottom', padx=10, pady=5, fill=tk.X)
# endregion

# region Build
build_label = ttk.Label(frame_build, textvariable=build_progress)
build_label.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
build_button = ttk.Button(frame_build, text='Build', command=build)
build_button.pack(anchor=tk.S, side='bottom', padx=10, pady=5, fill=tk.BOTH)
# endregion

window.mainloop()