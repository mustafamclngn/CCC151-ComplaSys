# Universal validator for all inputs

def all_fields_filled(fields):

    for field in fields:
        # QLineEdit 
        if hasattr(field, "text"):
            if not field.text().strip():
                return False
        # QTextEdit
        elif hasattr(field, "toPlainText"):
            if not field.toPlainText().strip():
                return False
        # QComboBox
        elif hasattr(field, "currentText"):
            if not field.currentText().strip():
                return False
    return True