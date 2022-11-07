from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical


class FileListPane(Static):

    def compose(self) -> ComposeResult:

        yield Vertical(
            Static("Title", classes="filelist-title" ),
            Static("Header", classes="filelist-header" ),
            Static("Items", classes="filelist-items" ),
            Static("Footer", classes="filelist-footer" ),
        )

class FileCommanderApp(App):

    CSS_PATH = "tmc.css"

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                FileListPane( classes="filelist-pane" ),
                FileListPane( classes="filelist-pane" ),
                classes="upper-pane",
            ),
            Static("Log pane", classes="lower-pane" ),
            Static("Status Bar", classes="status-bar" ),
        )

if __name__ == "__main__":
    app = FileCommanderApp()
    app.run()
