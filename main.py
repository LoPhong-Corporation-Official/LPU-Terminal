import ctypes
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import os

# -------------------------------
#  Load C++ DLL
# -------------------------------
dll = ctypes.CDLL("./SystemCore.dll")

# prototype: const char* ExecuteCommand(const char* input)
dll.ExecuteCommand.restype = ctypes.c_char_p
dll.ExecuteCommand.argtypes = [ctypes.c_char_p]

console = Console()

# -------------------------------
#  Terminal UI
# -------------------------------
def run_terminal():
    console.print(Panel.fit(" [bold cyan]LPU Terminal[/bold cyan] ", border_style="cyan"))

    while True:
        try:
            # Prompt đẹp
            cmd = console.input("[bold green]LPU>>>[/bold green] ").strip()

            if cmd == "":
                continue
            if cmd.lower() == "exit":
                console.print("[yellow]Exiting...[/yellow]")
                break

            # gửi vào DLL
            result_ptr = dll.ExecuteCommand(cmd.encode("utf-8"))
            result = result_ptr.decode("utf-8", errors="ignore")

            # xử lý lệnh clear
            if "{__CLR__}" in result:
                os.system("cls")
                continue

            # in kết quả đẹp
            console.print(Text(result, style="white"))

        except KeyboardInterrupt:
            console.print("\n[bold red]Dừng terminal.[/bold red]")
            break
        except Exception as e:
            console.print(f"[red]Eror: {e}[/red]")


if __name__ == "__main__":
    run_terminal()
