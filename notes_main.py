#start to create smart notes app
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json
app = QApplication([])

'''Notes in json'''
notes = {
    "Welcome!": 
    {
        "text": "This is the best note taking app in the world!",
        "tags": ["good", "instructions"]
    }
}

with open("notes_data.json", "w") as file:
    json.dump(notes, file)

'''Application interface'''
#application window parameters
notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)
#application window widgets
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')
button_note_create = QPushButton('Create note') #a window appears with the field "Enter note name"
button_note_del = QPushButton('Delete note')
button_note_save = QPushButton('Save note')
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')
field_text = QTextEdit()
button_add = QPushButton('Add to note')
button_del = QPushButton('Untag from note')
button_search = QPushButton('Search notes by tag')
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')
#arranging widgets by layout
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_search)
col_2.addLayout(row_3)
col_2.addLayout(row_4)
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def add_note():
    stupid_note, result = QInputDialog.getText(notes_win, "Add note", "Note name:")
    if stupid_note != "":
        notes[stupid_note] = {"text": "", "tags": []}
        list_notes.addItem(stupid_note)
        list_tags.addItems(notes[stupid_note]["tags"])
        print(notes)
button_note_create.clicked.connect(add_note)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        with open("notes_data.json" , "w") as file:
            json.dump(notes,file)
        list_notes.clear()
        field_text.clear()
        list_tags.clear()
        list_notes.addItems(notes)
button_note_del.clicked.connect(del_note)

def search_note():
    if button_search.text() == "Search notes by tag":
        tag = field_tag.text()
        poo = {}
        for n in notes:
            if tag in notes[n]['tags']:
                poo[n] = notes[n]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(poo)
        button_search.setText("Reset search")
    elif button_search.text() == "Reset search":
        list_notes.clear()
        list_tags.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        button_search.setText("Search note ")
button_search.clicked.connect(search_note)





def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        with open("notes_data.json" , "w") as file:
            json.dump(notes,file)
        list_tags.clear()
        list_tags.addItems(notes[key]['tags'])
button_del.clicked.connect(del_tag) 

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_data.json" , "w") as file:
                json.dump(notes,file)
button_note_save.clicked.connect(save_note)


'''Application functionality'''
def show_note():
    #get the text from the note with the title highlighted and display it in the edit field
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes[key]["tags"])

def add_tags():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tags = field_tag.text()
        if tags not in notes[key]['tags']:
            notes[key]["tags"].append(tags)
            list_tags.addItem(tags)
            field_tag.clear()
            with open("notes_data.json" , "w") as file:
                json.dump(notes,file)
button_add.clicked.connect(add_tags)

'''Run the application'''
#connecting event processing
list_notes.itemClicked.connect(show_note)
#run the application
with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

notes_win.show()
app.exec_()