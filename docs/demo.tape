Output docs/assets/demos/pythonlings-demo.gif

Set Shell "bash"
Set FontSize 18
Set Width 1200
Set Height 760
Set Padding 16
Set Framerate 16
Set TypingSpeed 35ms

# Hidden setup: a throwaway HOME so `pythonlings` creates a fresh ~/.pythonlings
# without touching the real one, from a non-workspace directory so zero-config
# resolution kicks in. None of this is recorded.
Hide
Type 'export HOME=/tmp/pythonlings-demo && rm -rf "$HOME" && mkdir -p "$HOME" && cd "$HOME" && clear'
Enter
Sleep 500ms
Show

# Zero-config: one command creates the workspace and opens the first exercise.
Type "pythonlings"
Enter
Sleep 3s

# Coding screen -> local Python reference (F5), then close it (Esc)
Escape
Type@0ms "[15~"
Sleep 2s
Escape
Sleep 700ms

# Topic picker (F4)
Escape
Type@0ms "OS"
Sleep 1.5s

# Quit back to the shell
Ctrl+Q
Sleep 800ms

# There's a CLI too: progress and hints
Type "pythonlings list"
Enter
Sleep 1.5s

Type "pythonlings hint variables1"
Enter
Sleep 1.8s
