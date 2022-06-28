import tkinter
from weakref import ref 
from PIL import ImageTk, Image
from matplotlib.backend_bases import LocationEvent

reference_x_location = 90
reference_y_location = 140
query_x_location = 90
query_y_location = 190
penalty_x_location = 90
penalty_y_location = 290
matching_score_x_location = 90
matching_score_y_location = 240


root = tkinter.Tk()
root.title("Needleman-Wunsch Algorithm")
root.geometry('600x600')



canv = tkinter.Canvas(root, width=80, height=80, bg='white')
canv.grid(row=2, column=3)
img = ImageTk.PhotoImage(Image.open("image/nw_background_image.jpeg"))  # PIL solution
canv.create_image(0, 0, anchor="nw", image=img)  
canv.pack(fill = "both", expand = True)


def draw_entry_and_label(x_location, y_location, label_text):
    canv_text = canv.create_text(x_location,y_location,font = ("Arial", 24, "bold"), fill= "white")
    canv.itemconfig(canv_text, text=label_text)

    # reference_label=tkinter.Label(root, text="reference: ", font = ("Arial", 24, "bold"))
    # reference_label.place(x= 50, y=150 )
    reference_input = tkinter.Entry(root,width = 20, borderwidth=0, font=("Arial", 24), bg = "white")
    reference_input.place(x=x_location+100, y = y_location-15)


draw_entry_and_label(reference_x_location, reference_y_location, "Reference: ") #draw reference entry box
draw_entry_and_label(query_x_location, query_y_location, "Query: ")
draw_entry_and_label(matching_score_x_location, matching_score_y_location, "Match Score: ")
draw_entry_and_label(penalty_x_location, penalty_y_location, "Penalty: ")
bt = tkinter.Button(text="Submit")
bt.place(x=270, y = penalty_y_location+50,bordermode="inside")




root.mainloop()