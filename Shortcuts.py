from PyQt5.QtCore import Qt

Key_Ctrl_Enter = "Ctrl + Enter"
Key_Alt_Enter = "Alt + Enter"
Key_Alt_BackSpace = "Alt + Backspace"
Key_Ctrl_R = "Ctrl + R"

shortcuts = {
    frozenset([Qt.Key_Control, Qt.Key_Return]) : Key_Ctrl_Enter,
    frozenset([Qt.Key_Control, Qt.Key_R]) : Key_Ctrl_R,
    frozenset([Qt.Key_Alt, Qt.Key_Return]) : Key_Alt_Enter,
    frozenset([Qt.Key_Alt, Qt.Key_Backspace]) : Key_Alt_BackSpace
}