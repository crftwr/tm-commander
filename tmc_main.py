import os
import fnmatch
import datetime

from rich.text import Text

from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from textual.widgets import TextLog
from textual.containers import Container, Horizontal, Vertical

import tmc_misc

# ---

class Item:

    def __init__( self, name, size, mtime ):
        self.name = name
        self.size = size
        self.mtime = mtime

# ---

class Filter:

    def __init__(self):
        pass

    def apply( self, items ):
        return items


class WildcardFilter(Filter):

    def __init__( self, include_patterns, exclude_patterns ):
        self.include_patterns = include_patterns
        self.exclude_patterns = exclude_patterns

    def apply( self, items ):
        
        def cond( item ):

            for include_pattern in self.include_patterns:
                if fnmatch.fnmatch( item.name, include_pattern ):
                    break
            else:
                return False

            for exclude_pattern in self.exclude_patterns:
                if fnmatch.fnmatch( item.name, exclude_pattern ):
                    return False

            return True

        return filter( cond, items )

# ---

class FileItemWidgeet(Static):

    def __init__( self, item, **args ):
        Static.__init__( self, **args )
        self.item = item
        self.selected = False

    def compose(self) -> ComposeResult:

        # TODO : 拡張子も別カラムに表示する

        s_size = "%6s" % tmc_misc.getFileSizeString(self.item.size)
        s_mtime = datetime.datetime.fromtimestamp(self.item.mtime).strftime( "%Y-%m-%d %H:%M:%S" )

        yield Static( "  ", classes="file-cursor" )
        yield Static( Text( self.item.name, no_wrap=True, overflow="ellipsis" ), classes="file-name" )
        yield Static( f" {s_size} {s_mtime}", classes="file-stats" )

    def show_cursor(self, show=True):

        cursor = self.query_one(".file-cursor")
        if show:
            cursor.update("▶︎ ")
        else:
            cursor.update("  ")

    def select( self, select=True ):

        self.selected = select

        if self.selected:
            self.add_class("selected")
        else:
            self.remove_class("selected")

class FileListWidget(Container):
    pass

class FileListPane( Static, can_focus=True, can_focus_children=False ):

    BINDINGS = [
        ("up", "move_cursor_prev", "Move cursor to previous item" ),
        ("down", "move_cursor_next", "Move cursor to next item" ),
        ("space", "select_single_item(1)", "Select or unselect single item and move cursor to next item" ),
    ]

    def __init__( self, **args ):
        Static.__init__( self, **args )

        self.location = "." # FIXME : ファイルリストクラスにする
        self.filter = WildcardFilter( include_patterns=["*"], exclude_patterns=[".*"] )

        self.cursor = 0

    def compose(self) -> ComposeResult:

        yield Vertical(
            Static( "Title", classes="filelist-title" ),
            Static( "Header", classes="filelist-header" ),
            FileListWidget( classes = "filelist-items" ),
            Static( "Footer", classes="filelist-footer" ),
        )

    def on_focus( self, event ):
        print("on_focus", event)
        self.action_update_cursor( advance=0 )

    def on_blur( self, event ):
        print("on_blur", event)
        self.action_update_cursor( advance=0, show=False )

    def action_update_cursor( self, advance, show=True ):

        container = self.query_one(".filelist-items")

        if self.cursor is not None:
            container.children[self.cursor].show_cursor(False)

        new_cursor = self.cursor + advance
        if new_cursor>=0 and new_cursor<len(container.children):
            self.cursor = new_cursor

        if show:
            container.children[self.cursor].show_cursor(True)

        container.children[self.cursor].scroll_visible()

    def action_move_cursor_prev(self):
        self.action_update_cursor( advance = -1 )

    def action_move_cursor_next(self):
        self.action_update_cursor( advance = 1 )

    def action_select_single_item( self, move_cursor ):
        
        if self.cursor is None: return

        container = self.query_one(".filelist-items")
        item_widget = container.children[self.cursor]
        item_widget.select( not item_widget.selected )

        if move_cursor == 1:
            self.action_move_cursor_next()
        elif move_cursor == -1:
            self.action_move_cursor_prev()

    def action_update_location( self, location ):

        self.location = location
        self.query_one(".filelist-title").update(location)

        items_listed = []
        for filename in os.listdir( self.location ):
            fullpath = os.path.join( self.location, filename )
            st = os.stat( fullpath )
            items_listed.append( Item(filename, st.st_size, st.st_mtime) )

        items_filtered = self.filter.apply( items_listed )
        items_sorted = items_filtered

        container = self.query_one(".filelist-items")
        container.query( ".filelist-item" ).remove()

        for item in items_sorted:
            item = FileItemWidgeet( item, classes="filelist-item" )
            container.mount(item)

class LogPane( TextLog, can_focus=False, can_focus_children=False ):
    pass

class FileCommanderApp(App):

    CSS_PATH = "tmc.css"

    BINDINGS = [
        ("d",   "goto()", "Goto"),
        ("l",   "log()", "Log"),
        ("q",   "quit()", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                FileListPane( id="left-pane", classes="filelist-pane" ),
                FileListPane( id="right-pane", classes="filelist-pane" ),
                classes="upper-pane",
            ),
            LogPane( id="lower-pane", classes="log-pane", max_lines=10000 ),
            Static("Status Bar", classes="status-bar" ),
        )

    def on_mount(self):
        #self.query_one("#left-pane").focus()
        self.action_goto()

    def action_log(self):
        self.query_one("#lower-pane").write( datetime.datetime.now().isoformat() )

    def action_goto(self):
        self.query_one("#left-pane").action_update_location( location = os.path.abspath("./test-data/Folder1") )
        self.query_one("#right-pane").action_update_location( location = os.path.abspath("./test-data/Folder2") )


if __name__ == "__main__":
    app = FileCommanderApp()
    app.run()
