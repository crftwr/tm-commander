from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical

class FileCommanderApp(App):

    CSS_PATH = "tmc.css"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                Static("Left pane", classes="filelist-pane" ),
                Static("Right pane", classes="filelist-pane" ),
                classes="upper-pane",
            ),
            Static("Log pane", classes="lower-pane" ),
            Static("Status Bar", classes="status-bar" ),
        )

if __name__ == "__main__":
    app = FileCommanderApp()
    app.run()
