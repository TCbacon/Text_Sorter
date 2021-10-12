import tkinter as tk
from TkinterDnD2 import DND_FILES, TkinterDnD
from tkinter import scrolledtext
import tkinter.filedialog as file_dialog
from tkinter.messagebox import askokcancel, showinfo, WARNING
import re
import string

#list holding contents from text file
word_list = []
#list to compare first letter to put space in between different alphabets
ALPHABET_LIST = string.printable

#lower case box boolean
is_lower_checked = False


#popup copy paste menu right click
def do_popup_menu(event):
    w = event.widget
    context_menu.post(event.x_root, event.y_root)
    context_menu.entryconfigure("Cut", command=lambda: w.event_generate("<<Cut>>"))
    context_menu.entryconfigure("Copy", command=lambda: w.event_generate("<<Copy>>"))
    context_menu.entryconfigure("Paste", command=lambda: w.event_generate("<<Paste>>"))

def drop_inside_textbox(event):
    
    #clear previous dropped file context from word list to prevent clutter
    word_list.clear()

    #to remove the curly braces in data path
    data_path = re.sub('{|}', "",event.data)

    input_box.delete("1.0", "end")
    if data_path.endswith(".txt"):
        with open(data_path, 'r') as file:
            for line in file:
                line = line.strip()
                input_box.insert('end', f"{line}\n")

                #prevent adding empty lines to list of text
                if len(line) > 0:
                    word_list.append(line)
        
    else:
        input_box.insert('end', 'Does not have extension txt')

# to sort and put space between different alphabet starting word
def alphabet_space_sort(out_box, w_list):
    alpha_index =0 
    out_box.delete('1.0', tk.END)
    w_list_lower = []

    #convert items in list to lower case 
    if is_lower_checked:
        w_list_lower = [item.lower() for item in w_list]
    else:
        w_list_lower = w_list

    #sort the list in alphabetical order
    w_list_lower.sort()   

    #add space if next word in row does not start with same letter as the previous row 
    for line in w_list_lower:
        if line[0] in ALPHABET_LIST and line[0] != ALPHABET_LIST[alpha_index]:
            alpha_index = ALPHABET_LIST.index(line[0])    
            line = '\n' + line 
            
        out_box.insert(tk.END, line +'\n')
    
    #remove first line in output box if there is whitespace
    if out_box.get('1.0','2.0').isspace():
        out_box.delete('1.0','2.0')

    #clear word list after each sort to prevent clutter from previous text
    word_list.clear()


#checkbox lower case
def checkbox_lower():
    #global so boolean effect is not just local to this function
    global is_lower_checked

    if checkbox_value.get() == 1:
        is_lower_checked = True
    elif checkbox_value.get() == 0:
        is_lower_checked = False

# sort file with sort button
def sort_file():
    if input_box.compare('end-1c', "==", "1.0"):
        output_tbox.delete('1.0', tk.END)
        output_tbox.insert('end', 'Input is empty add a file to it.')
    
    elif len(word_list) > 0:
        try:
            alphabet_space_sort(output_tbox, word_list)
        except IndexError:
            output_tbox.delete('1.0', tk.END)
            output_tbox.insert('end', 'An error occured, please try again.')
   
    else:
        output_tbox.delete('1.0', tk.END) #clear text in field
        #split the texts on each line from input box and puts it in a list
        typed_text_list = input_box.get('1.0', tk.END).splitlines()
       
        #remove blank string from list
        while "" in typed_text_list:
            typed_text_list.remove("")

        try:
            if len(typed_text_list) > 0:
                alphabet_space_sort(output_tbox, typed_text_list)
        
        except IndexError:
            output_tbox.delete('1.0', tk.END)
            output_tbox.insert('end', 'An error occured, please try again.')
            

#save sorted file
def save_file(output_box):
    files_ext = [('Text Document', '*.txt'),('All Files', '*.*'),  
             ('Python Files', '*.py')
             ] 

    file = file_dialog.asksaveasfile(filetypes = files_ext, mode='w', defaultextension= files_ext)

    # close dialog box if cancel pressed
    if file is None:
        return

    text2save = str(output_box.get(1.0, tk.END))
    file.write(text2save)
    file.close()


#press button to switch frames or scenes
def show_frame(f):
    f.tkraise()

#back to main app
def back_to_main(f):
    f.tkraise()

#confirm exit app
def confirm_close_app():
    answer = askokcancel(
        title='Close the App?',
        message='Click OK to confirm',
        icon=WARNING)

    if answer:
        close_app()

#close app
def close_app():
    root.destroy()
  


#creating window
root = TkinterDnD.Tk()
root.title('Text Sorter')
root.iconbitmap('C:\VScode Tkinter exe\/text_sorter.ico')
root.geometry('900x600')

#about page frame
about_frame = tk.Frame(root, bg = '#9EA097')
about_frame.grid(row=0, column=0, sticky="news", columnspan=2)
about_to_main_btn = tk.Button(about_frame, text='Back',command=lambda:back_to_main(main_app_frame))
about_to_main_btn.grid(row=0, column=0)
about_label = tk.Label(about_frame, text="Made by TCbacon © 2021", bg = 'white')
about_label.grid(row=1,column=1)


#help page frame
help_frame = tk.Frame(root, bg = '#6e76c1')
help_frame.grid(row=0, column=0, sticky="news", columnspan=2)
help_to_main_btn = tk.Button(help_frame, text='Back',command=lambda:back_to_main(main_app_frame))
help_to_main_btn.grid(row=0, column=0)
about_label = tk.Label(help_frame, text="Instructions:\n\u2022 Drag and drop a .txt file into the input box and click " + 
"sort button to show result in the output box.\n"+ 
"\u2022 Toggle the checkbox on to lower case all letters, and toggle off to leave the text as is.\n" +
"\u2022 When satisfied with output, click the save button to save the sorted file to a location on the computer.", font='Helvetica 12 bold', borderwidth=2, relief="solid", justify=tk.LEFT, anchor='w')
about_label.grid(row=1,column=1)


#main app frame
main_app_frame = tk.Frame(root, bg='#c6d9e0')
main_app_frame.grid(row=0, column=0, sticky="news", columnspan=2, ipadx = root.winfo_screenwidth(), ipady = root.winfo_screenheight())


#switch frames
for frame in (main_app_frame, about_frame, help_frame):
    frame.grid(row=0, column=0, sticky='news')


#KEYBOARD for copy, paste, redo
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Cut")
context_menu.add_command(label="Copy")
context_menu.add_command(label="Paste")
root.bind("<Button-3>", do_popup_menu)


#buttons on top of list view
help_button = tk.Button(main_app_frame,text='Help', command=lambda:show_frame(help_frame))
help_button.grid(row=0, column=0)
about_button = tk.Button(main_app_frame ,text='About', command=lambda:show_frame(about_frame))
about_button.grid(row=0, column=1, padx=(1,0))

#quit button
quit_btn = tk.Button(main_app_frame, text='Exit', command=confirm_close_app)
quit_btn.grid(row=0, column=4,ipadx = 20)

#title in app
title_lbl = tk.Label(main_app_frame, text='Text Sorter', font='helvetica 16 bold')
title_lbl.grid(row=0, column=2, columnspan=2)

#input textbox drag and drop file
input_label = tk.Label(main_app_frame, text='Input')
input_label.grid(row=2, column=2)
input_box = scrolledtext.ScrolledText(main_app_frame, width=40, height=20, undo=True)
input_box.drop_target_register(DND_FILES)
input_box.dnd_bind("<<Drop>>", drop_inside_textbox)
input_box.grid(row=4, column=2, rowspan=4, padx=(0,10))


#output textbox
output_label = tk.Label(main_app_frame, text='Output')
output_label.grid(row=2, column=3)
output_tbox = scrolledtext.ScrolledText(main_app_frame, width=40, height=20, undo=True)
output_tbox.grid(row=4, column=3, rowspan=4)


#button for sorting file
#checkbox for uppder to lower case
checkbox_value = tk.IntVar()

checkbox_lower_case = tk.Checkbutton(main_app_frame, text='Lower Case All', variable = checkbox_value, onvalue=1,offvalue=0, command=checkbox_lower)
checkbox_lower_case.grid(row=5, column=4, padx=(20,0), pady=(100,0), ipady=2)
save_button = tk.Button(main_app_frame,text='Save', width=10, height=3, command=lambda:save_file(output_tbox))
save_button.grid(row=6, column=4, padx=(20,0))
sort_button = tk.Button(main_app_frame,text='Sort',command=sort_file, width=10, height=3)
sort_button.grid(row=7, column=4, padx=(20,0))


main_app_frame.tkraise()
root.mainloop()