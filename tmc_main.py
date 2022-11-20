import os
import fnmatch
import datetime

from rich.text import Text

from textual.app import App, ComposeResult, RenderResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from textual.containers import Container, Horizontal, Vertical

import tmc_misc

# ---

class Item:

    def __init__( self, name, size, mtime ):
        self.name = name
        self.size = size
        self.mtime = mtime


"""
class FileItem(Item):

    def __init__( self, name, size, mtime ):
        Item.__init__( self, name, size, mtime )
"""


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

    def compose(self) -> ComposeResult:

        # TODO : 拡張子も別カラムに表示する

        s_size = "%6s" % tmc_misc.getFileSizeString(self.item.size)
        s_mtime = datetime.datetime.fromtimestamp(self.item.mtime).strftime( "%Y-%m-%d %H:%M:%S" )

        yield Static( Text( self.item.name, no_wrap=True, overflow="ellipsis" ), classes="file-name" )
        yield Static( f" {s_size} {s_mtime}", classes="file-stats" )


class FileListPane(Static):

    def __init__( self, **args ):
        Static.__init__( self, **args )

        self.location = "." # FIXME : ファイルリストクラスにする
        self.filter = WildcardFilter( include_patterns=["*"], exclude_patterns=[".*"] )

    def compose(self) -> ComposeResult:

        yield Vertical(
            Static( "Title", classes="filelist-title" ),
            Static( "Header", classes="filelist-header" ),
            Container( classes = "filelist-items" ),
            Static( "Footer", classes="filelist-footer" ),
        )

    def action_update( self, location ):

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


class FileCommanderApp(App):

    CSS_PATH = "tmc.css"

    BINDINGS = [
        ("d", "goto()", "Goto"),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Horizontal(
                FileListPane( id="left-pane", classes="filelist-pane" ),
                FileListPane( id="right-pane", classes="filelist-pane" ),
                classes="upper-pane",
            ),
            Static("Log pane", classes="lower-pane" ),
            Static("Status Bar", classes="status-bar" ),
        )

    def action_goto( self ):
        print( "Goto action" )
        self.query_one("#left-pane").action_update( location = "/Users/crftwr" )


if __name__ == "__main__":
    app = FileCommanderApp()
    app.run()
