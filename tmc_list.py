

from rich.text import Text

from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen

# ---

class ListItemWidgeet(Static):
    def __init__( self, **args ):
        super().__init__( **args )

class ListWidget(Container):
    pass

class ListScreen(Screen):

    BINDINGS = [
        ("up", "move_cursor_prev", "Move cursor to previous item" ),
        ("down", "move_cursor_next", "Move cursor to next item" ),
        ("enter", "decide()", "Decide"),
        ("escape", "cancel()", "Cancel"),
    ]

    def __init__( self, items, callback, **args ):
        super().__init__( **args )

        self.items = items
        self.callback = callback
        self.cursor = None

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static( "Title", classes="dialog-title-bar" ),
            ListWidget( classes = "dialog-list-items" ),
            Static( "Footer", classes="dialog-status-bar" ),
            classes = "list-dialog",
        )

    def on_mount(self):
        
        list_widget = self.query_one(".dialog-list-items")

        for item in self.items:
            item_widget = ListItemWidgeet( renderable=Text( item[0], no_wrap=True, overflow="ellipsis" ), classes="filelist-item" )
            list_widget.mount(item_widget)

        self.cursor = 0

        self.action_update_cursor(0)

    def action_update_cursor( self, advance ):

        list_widget = self.query_one(".dialog-list-items")

        if self.cursor is not None:
            list_widget.children[self.cursor].remove_class("selected")

        new_cursor = self.cursor + advance
        if new_cursor>=0 and new_cursor<len(list_widget.children):
            self.cursor = new_cursor

        list_widget.children[self.cursor].add_class("selected")
        list_widget.children[self.cursor].scroll_visible()

    def action_move_cursor_prev(self):
        self.action_update_cursor( advance = -1 )

    def action_move_cursor_next(self):
        self.action_update_cursor( advance = 1 )

    def action_decide(self):
        print("Decide")
        self.app.pop_screen()
        item = self.items[self.cursor]
        self.callback(item)

    def action_cancel(self):
        print("Cancel")
        self.app.pop_screen()
        self.callback( None )

    def action_debug(self):
        print( "Screen stack :", self.app.screen_stack )
        print( "Focus chain :", self.screen.focus_chain )

