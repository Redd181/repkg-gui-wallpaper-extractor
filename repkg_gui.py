import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import threading
from pathlib import Path


class RepkgGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RePKG GUI - Wallpaper Engine PKG Extractor")
        self.root.geometry("900x700")

        # 存储repkg.exe路径
        self.repkg_exe_path = ""

        self.create_widgets()

    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # RePKG.exe 路径选择
        exe_frame = ttk.Frame(main_frame)
        exe_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(exe_frame, text="RePKG.exe 路径:").pack(side=tk.LEFT)
        self.exe_path_var = tk.StringVar()
        exe_entry = ttk.Entry(exe_frame, textvariable=self.exe_path_var)
        exe_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Button(exe_frame, text="浏览", command=self.browse_exe).pack(side=tk.RIGHT)

        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Extract 选项卡
        self.create_extract_tab(notebook)

        # Info 选项卡
        self.create_info_tab(notebook)

        # 日志输出区域
        log_frame = ttk.LabelFrame(main_frame, text="输出日志", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # 清除日志按钮
        ttk.Button(log_frame, text="清除日志", command=self.clear_log).pack()

    def create_extract_tab(self, notebook):
        # Extract 选项卡
        extract_frame = ttk.Frame(notebook, padding="10")
        notebook.add(extract_frame, text="提取/转换")

        # 使用 pack 布局管理器
        # 输入文件/目录
        input_frame = ttk.Frame(extract_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(input_frame, text="输入文件/目录:").pack(side=tk.LEFT)
        self.input_path_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_path_var)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Button(input_frame, text="浏览", command=self.browse_input).pack(side=tk.RIGHT)

        # 输出目录
        output_frame = ttk.Frame(extract_frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_path_var = tk.StringVar(value="./output")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Button(output_frame, text="浏览", command=self.browse_output).pack(side=tk.RIGHT)

        # 选项框架
        options_frame = ttk.LabelFrame(extract_frame, text="选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))

        # 使用 grid 布局在选项框架内
        self.recursive_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="递归搜索子目录 (-r)", variable=self.recursive_var).grid(row=0, column=0,
                                                                                                     sticky=tk.W,
                                                                                                     pady=2)

        self.tex_mode_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="TEX 转换模式 (-t)", variable=self.tex_mode_var).grid(row=0, column=1,
                                                                                                  sticky=tk.W, pady=2,
                                                                                                  padx=(20, 0))

        self.single_dir_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="单目录输出 (-s)", variable=self.single_dir_var).grid(row=1, column=0,
                                                                                                  sticky=tk.W, pady=2)

        self.copy_project_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="复制项目文件 (-c)", variable=self.copy_project_var).grid(row=1, column=1,
                                                                                                      sticky=tk.W,
                                                                                                      pady=2,
                                                                                                      padx=(20, 0))

        self.use_name_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="使用项目名称 (-n)", variable=self.use_name_var).grid(row=2, column=0,
                                                                                                  sticky=tk.W, pady=2)

        self.no_tex_convert_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="不转换 TEX (--no-tex-convert)", variable=self.no_tex_convert_var).grid(
            row=2, column=1, sticky=tk.W, pady=2, padx=(20, 0))

        self.overwrite_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="覆盖现有文件 (--overwrite)", variable=self.overwrite_var).grid(row=3,
                                                                                                            column=0,
                                                                                                            sticky=tk.W,
                                                                                                            pady=2)

        self.debug_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="调试信息 (-d)", variable=self.debug_var).grid(row=3, column=1, sticky=tk.W,
                                                                                           pady=2, padx=(20, 0))

        # 文件扩展名过滤
        filter_frame = ttk.Frame(options_frame)
        filter_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(filter_frame, text="忽略扩展名 (-i):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ignore_exts_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.ignore_exts_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E),
                                                                                  padx=5)

        ttk.Label(filter_frame, text="仅提取扩展名 (-e):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.only_exts_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.only_exts_var, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E),
                                                                                padx=5)

        filter_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(1, weight=1)

        # 执行按钮 - 放在最后，确保可见
        button_frame = ttk.Frame(extract_frame)
        button_frame.pack(fill=tk.X, pady=10)

        extract_button = ttk.Button(button_frame, text="开始提取", command=self.run_extract)
        extract_button.pack(pady=10)

        # 设置按钮样式
        extract_button.configure(style='Accent.TButton')

    def create_info_tab(self, notebook):
        # Info 选项卡
        info_frame = ttk.Frame(notebook, padding="10")
        notebook.add(info_frame, text="信息查看")

        # 输入文件
        input_frame = ttk.Frame(info_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="输入文件:").pack(side=tk.LEFT)
        self.info_input_var = tk.StringVar()
        info_entry = ttk.Entry(input_frame, textvariable=self.info_input_var)
        info_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Button(input_frame, text="浏览", command=self.browse_info_input).pack(side=tk.RIGHT)

        # Info 选项
        info_options_frame = ttk.LabelFrame(info_frame, text="选项", padding="10")
        info_options_frame.pack(fill=tk.X, pady=(0, 10))

        self.info_sort_var = tk.BooleanVar()
        ttk.Checkbutton(info_options_frame, text="排序 (-s)", variable=self.info_sort_var).grid(row=0, column=0,
                                                                                                sticky=tk.W, pady=2)

        self.info_tex_var = tk.BooleanVar()
        ttk.Checkbutton(info_options_frame, text="TEX 目录信息 (-t)", variable=self.info_tex_var).grid(row=0, column=1,
                                                                                                       sticky=tk.W,
                                                                                                       pady=2,
                                                                                                       padx=(20, 0))

        self.print_entries_var = tk.BooleanVar()
        ttk.Checkbutton(info_options_frame, text="打印条目 (-e)", variable=self.print_entries_var).grid(row=1, column=0,
                                                                                                        sticky=tk.W,
                                                                                                        pady=2)

        ttk.Label(info_options_frame, text="排序方式 (-b):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sort_by_var = tk.StringVar(value="name")
        sort_combo = ttk.Combobox(info_options_frame, textvariable=self.sort_by_var,
                                  values=["name", "extension", "size"], state="readonly", width=15)
        sort_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0))

        ttk.Label(info_options_frame, text="项目信息键 (-p):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.project_info_var = tk.StringVar()
        ttk.Entry(info_options_frame, textvariable=self.project_info_var, width=30).grid(row=3, column=1,
                                                                                         sticky=(tk.W, tk.E), padx=5)

        ttk.Label(info_options_frame, text="标题过滤 (--title-filter):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.title_filter_var = tk.StringVar()
        ttk.Entry(info_options_frame, textvariable=self.title_filter_var, width=30).grid(row=4, column=1,
                                                                                         sticky=(tk.W, tk.E), padx=5)

        info_options_frame.columnconfigure(1, weight=1)

        # 执行按钮 - 放在最后，确保可见
        button_frame = ttk.Frame(info_frame)
        button_frame.pack(fill=tk.X, pady=10)

        info_button = ttk.Button(button_frame, text="查看信息", command=self.run_info)
        info_button.pack(pady=10)

        # 设置按钮样式
        info_button.configure(style='Accent.TButton')

    def browse_exe(self):
        filename = filedialog.askopenfilename(
            title="选择 RePKG.exe",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if filename:
            self.exe_path_var.set(filename)
            self.repkg_exe_path = filename

    def browse_input(self):
        # 可以选择文件或目录
        choice = messagebox.askyesno("选择输入", "选择 '是' 来选择文件，'否' 来选择目录")
        if choice:
            filename = filedialog.askopenfilename(
                title="选择输入文件",
                filetypes=[("PKG文件", "*.pkg"), ("TEX文件", "*.tex"), ("所有文件", "*.*")]
            )
            if filename:
                self.input_path_var.set(filename)
        else:
            dirname = filedialog.askdirectory(title="选择输入目录")
            if dirname:
                self.input_path_var.set(dirname)

    def browse_output(self):
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_path_var.set(dirname)

    def browse_info_input(self):
        filename = filedialog.askopenfilename(
            title="选择要查看信息的文件",
            filetypes=[("PKG文件", "*.pkg"), ("TEX文件", "*.tex"), ("所有文件", "*.*")]
        )
        if filename:
            self.info_input_var.set(filename)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def run_extract(self):
        if not self.repkg_exe_path or not os.path.exists(self.repkg_exe_path):
            messagebox.showerror("错误", "请先选择有效的 RePKG.exe 文件")
            return

        if not self.input_path_var.get():
            messagebox.showerror("错误", "请选择输入文件或目录")
            return

        # 构建命令
        cmd = [self.repkg_exe_path, "extract", self.input_path_var.get()]

        # 添加选项
        if self.output_path_var.get():
            cmd.extend(["-o", self.output_path_var.get()])

        if self.recursive_var.get():
            cmd.append("-r")

        if self.tex_mode_var.get():
            cmd.append("-t")

        if self.single_dir_var.get():
            cmd.append("-s")

        if self.copy_project_var.get():
            cmd.append("-c")

        if self.use_name_var.get():
            cmd.append("-n")

        if self.no_tex_convert_var.get():
            cmd.append("--no-tex-convert")

        if self.overwrite_var.get():
            cmd.append("--overwrite")

        if self.debug_var.get():
            cmd.append("-d")

        if self.ignore_exts_var.get():
            cmd.extend(["-i", self.ignore_exts_var.get()])

        if self.only_exts_var.get():
            cmd.extend(["-e", self.only_exts_var.get()])

        # 在新线程中运行命令
        threading.Thread(target=self.execute_command, args=(cmd,), daemon=True).start()

    def run_info(self):
        if not self.repkg_exe_path or not os.path.exists(self.repkg_exe_path):
            messagebox.showerror("错误", "请先选择有效的 RePKG.exe 文件")
            return

        if not self.info_input_var.get():
            messagebox.showerror("错误", "请选择要查看信息的文件")
            return

        # 构建命令
        cmd = [self.repkg_exe_path, "info", self.info_input_var.get()]

        # 添加选项
        if self.info_sort_var.get():
            cmd.append("-s")

        if self.info_tex_var.get():
            cmd.append("-t")

        if self.print_entries_var.get():
            cmd.append("-e")

        if self.sort_by_var.get() != "name":
            cmd.extend(["-b", self.sort_by_var.get()])

        if self.project_info_var.get():
            cmd.extend(["-p", self.project_info_var.get()])

        if self.title_filter_var.get():
            cmd.extend(["--title-filter", self.title_filter_var.get()])

        # 在新线程中运行命令
        threading.Thread(target=self.execute_command, args=(cmd,), daemon=True).start()

    def execute_command(self, cmd):
        try:
            self.log_message(f"执行命令: {' '.join(cmd)}")
            self.log_message("=" * 50)

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace'
            )

            # 实时显示输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log_message(output.strip())

            # 获取返回码
            return_code = process.poll()
            self.log_message("=" * 50)
            if return_code == 0:
                self.log_message("命令执行成功!")
            else:
                self.log_message(f"命令执行失败，返回码: {return_code}")

        except Exception as e:
            self.log_message(f"执行命令时发生错误: {str(e)}")


def main():
    root = tk.Tk()

    # 设置样式
    style = ttk.Style()
    try:
        style.theme_use('clam')  # 使用更现代的主题
    except:
        pass

    app = RepkgGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()