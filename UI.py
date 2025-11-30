from textual.app import App, ComposeResult
from textual.widgets import Static, Input
from textual.containers import Vertical, Horizontal
from textual import events
from textual.widgets import Label
from textual.widget import Widget
from rich.text import Text

# ==========================
# Popup Message Box
# ==========================
class MessageBox(Static):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(f"[bold yellow]{self.message}[/bold yellow]")
        yield Static("\n[Press ESC to close]")

    def key_escape(self) -> None:
        self.remove()


# ==========================
# Main UI
# ==========================
class TerminalUI(App):

    CSS = """
    #root {
        background: black;
    }
    #output {
        border: solid green;
        height: 80%;
        color: white;
        padding: 1;
    }
    #input_bar {
        height: 20%;
        border: solid cyan;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            self.output = Static("Welcome to LNPLib Terminal!\n", id="output")
            yield self.output
            with Horizontal(id="input_bar"):
                self.input = Input(placeholder="Enter command here...")
                yield self.input

    # ==========================
    # Xử lý Enter
    # ==========================
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip()
        self.input.value = ""

        # --- FIX QUAN TRỌNG: dùng .text thay .renderable ---
        old_text = self.output.text
        new_text = old_text + f"\n> {cmd}"
        self.output.update(Text(new_text))

        # =====================
        #   Xử lý lệnh
        # =====================
        if cmd == "popup":
            self.mount(MessageBox("This is a popup message!"))

        elif cmd == "clear":
            self.output.update(Text(""))

        else:
            self.output.update(
                Text(self.output.text + "\nUnknown command.")
            )

    # ==========================
    # Điều khiển bằng phím mũi tên
    # ==========================
    async def on_key(self, event: events.Key) -> None:

        if event.key == "up":
            self.output.update(Text(self.output.text + "\n[Arrow Up pressed]"))

        elif event.key == "down":
            self.output.update(Text(self.output.text + "\n[Arrow Down pressed]"))

        elif event.key == "f2":
            self.mount(MessageBox("Menu:\n- About\n- Settings\n- Exit"))


if __name__ == "__main__":
    TerminalUI().run()
