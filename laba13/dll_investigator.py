import ctypes
import sys


LPCWSTR = ctypes.c_wchar_p
HANDLE  = ctypes.c_void_p

print("--- Загрузка kernel32.dll ---")
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


kernel32.LoadLibraryW.restype  = HANDLE
kernel32.LoadLibraryW.argtypes = [LPCWSTR]

kernel32.GetProcAddress.restype  = HANDLE
kernel32.GetProcAddress.argtypes = [HANDLE, ctypes.c_char_p]

kernel32.FreeLibrary.argtypes = [HANDLE]

print("\n--- Проецирование user32.dll ---")
dll_name = "user32.dll"
h_module = kernel32.LoadLibraryW(dll_name)

if not h_module:
    print(f"[ОШИБКА] Не удалось загрузить библиотеку. Код: {ctypes.get_last_error()}")
    sys.exit(1)

print(f"[УСПЕХ] Библиотека {dll_name} загружена")
print(f"[НИЗКИЙ УРОВЕНЬ] HMODULE (базовый адрес): {hex(h_module)}")

print("\n--- Поиск MessageBoxW в Таблице Экспорта ---")
func_name = b"MessageBoxW"
func_address = kernel32.GetProcAddress(h_module, func_name)

if not func_address:
    print(f"[ОШИБКА] Функция не найдена. Код: {ctypes.get_last_error()}")
    kernel32.FreeLibrary(h_module)
    sys.exit(1)

print(f"[УСПЕХ] Функция найдена")
print(f"[НИЗКИЙ УРОВЕНЬ] Адрес MessageBoxW: {hex(func_address)}")

print("\n--- Вызов функции по адресу ---")
# MessageBoxW(HWND, LPCWSTR, LPCWSTR, UINT)
MessageBoxW = ctypes.WINFUNCTYPE(
    ctypes.c_int,      
    HANDLE,            
    LPCWSTR,           
    LPCWSTR,           
    ctypes.c_uint      
)(func_address)

print("[ПРОЦЕССОР] Выполняем CALL...")
MessageBoxW(None, "Сообщение вызвано через прямой адрес из Таблицы Экспорта!", "Системное программирование", 0)

print("\n--- Выгрузка ---")
kernel32.FreeLibrary(h_module)
print("[УСПЕХ] Модуль выгружен")