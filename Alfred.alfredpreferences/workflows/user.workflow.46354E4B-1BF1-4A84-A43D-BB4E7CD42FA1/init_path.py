import os
import sys
import datetime as dt
import getpass
import subprocess

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建lib目录的绝对路径
lib_path = os.path.join(current_dir, "lib")

# 将lib目录添加到sys.path
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)


def install_package(package):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package, "--target", lib_path]
    )


def load_cffi_backend():
    python_version = f"{sys.version_info.major}{sys.version_info.minor}"
    backend_name = f"_cffi_backend.cpython-{python_version}-darwin.so"
    backend_path = os.path.join(lib_path, backend_name)

    if not os.path.exists(backend_path):
        #     spec = importlib.util.spec_from_file_location("_cffi_backend", backend_path)
        #     module = importlib.util.module_from_spec(spec)
        #     spec.loader.exec_module(module)
        #     sys.modules["_cffi_backend"] = module
        # else:
        install_package("cffi")


# 调用函数加载CFFI后端
load_cffi_backend()
