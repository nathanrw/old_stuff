_______________________________________________________________________________

            __   _____ __   _  ____  __     ____  _    _ __    __
           |  | |     |  \ | |/    \|  |   /  _ \| |  | |  \  /  |
           |  | |/| |\|   \| |  /\  \  |  /  / \_\ |  | |   \/   |
           |  | /|| | | \  \ | (  )  ) | /|  _| _| |  | | |\  /| |
           |  |/ || |/| |\   |  \/  /  |/ |  \_/ /  \/  / | \/ | |
           |_____|____|_| \__|\____/|_____|\____/ \____/|_|    |_|
                       _______  _______    __________
                      |       |/  _ \  \  /  /       |
                      | /| |\ |  / \_\  \/  /| /| |
                      |/ | | \|  _| _ )    ( |/ | | \|
                         | |  \  \_/ /  /\  \   | |
                         |_|   \____/__/  \__\  |_|
                    ____  ____  _____ _______  ____  ____
                   /  _ \|  _ \|     |       |/    \| __ \
                  /  / \_\ | \ \/| |\| /| |\ |  /\  \ |_) )
                 (   _| _| |  ) )| | |/ | | \| (  )  )   /
                  \  \_/ / |_/ /\| |/|  | |  \  \/  / |\ \
                   \____/|____/|_____|  |_|   \____/|_| \_\

_______________________________________________________________________________
Text Editor version: 0.10.0
copyright (c) 2002, 2003 by Peterpaul Klein Haneveld
e-mail:         pp_kl_h@hotmail.com
website:        www.kleinhaneveld.tk
_______________________________________________________________________________
This is a text editor with simple functionality, like notepad.

I don't think it's very hard to work with this editor, most things work exactly
the same as on other editors. The only thing you might get used to is the fact
there's no word-wrap option. This isn't possible due to the way the text is
stored in memory: in a matrix. This matrix has a width of 256 characters. While
it might be anoying while writing normal texts, it isn't while using this editor
for programming. For those of you who use ConTEXT (the editor i normally use
for coding), ConTEXT works the same way.

All options, like opening or saving a file, are available from the menu, opened
with the menu-button in the right-top corner. Some options from the menu are
also available as control-key combinations or with function keys. In the menu
this is displayed as: c-[key] or F1 ... F12. The chosen combinations are, for
what i know, the most used combinations nowadays, like: c-X, c-C, c-V for cut,
copy and paste. Look at the end of this file for a description of all the
possibilities. I have the plan to eventually add support for a configuration-
file, where these key combinations can be personalised. For now you just have
to do it with these combinations.

When you have suggestions or comments, or you've found a bug, please let me
know. You can e-mail me at pp_kl_h@hotmail.com.
_______________________________________________________________________________
Cursor Keys:
- [left]:       move cursor one position left
- [up]:         move cursor one position up
- [right]:      move cursor one position right
- [down]:       move cursor one position down

Special keys:
- [pgup]:       move cursor one page up
- [pgdn]:       move cursor one page down
- [home]:       move cursor to begin of line
- [end]:        move cursor to end on line

Function keys:
- [F3]:         find next
- [F4]:         replace current selection and find next

Edit keys:
- [insert]:     toggle insert/overwrite mode
- [delete]:     delete current character or delete selection
- [backspace]:  delete previous character or delete selection

Selecting text:
- Hold down the Shift-key in combination with one of the special or cursor keys.
- Use the mousepointer.

Control-key combinations:
- Ctrl-n:       New file
- Ctrl-o:       Reopen file
- Ctrl-s:       Save file
- Ctrl-x:       Cut
- Ctrl-c:       Copy
- Ctrl-v:       Paste
- Ctrl-f:       Find from top
- Ctrl-r:       Replace from top
- Ctrl-h:       Replace all
- Ctrl-z:       Undo
- Ctrl-y:       Redo
- Ctrl-a:       Select all
- Ctrl-[left]:  Move cursor to previous word
- Ctrl-[right]: Move cursor to next word
