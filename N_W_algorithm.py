import pandas as pd
import tkinter
from PIL import ImageTk, Image



"""
The Needleman-Wunsch Algorithm for global alignment of nucleotides


"""

def initializaiton_2(reference, query):
    len_reference = len(reference)
    len_query = len(query)
    list_reference = ["-","-"] + list(reference)
    list_query = ["-","-"] + list(query)
    big_matrix = []
    for row in range(0, len_query+2):
        submatrix = []
        for columns in range(0,len_reference+2):
            submatrix.append(0)
        big_matrix.append(submatrix)
        
    for i in range(2,(len_reference+2),1):
        big_matrix[0][i] = list_reference[i]
    for j in range(2, (len_query+2), 1):
        big_matrix[j][0] = list_query[j]
    for t in range(1,(len_reference+1),1):
        big_matrix[1][t+1] = penalty*t
    for s in range(1,(len_query+1),1):
        big_matrix[s+1][1]= penalty*s
        
    return big_matrix



def scoring(reference,query):
    array = initializaiton_2(reference, query)
    row = len(array)
    columns = len(array[0])
    #print(row, columns)
    
    "This dictionary stores the position where the score comes \
    from. It will be used for backracing.- Diagonal: 0, Left: 1, Top: 2"
    
    backtrace_dict = {}
    for p in range(1,row):
        for q in range(1,columns):
            if p > 1 and q > 1:
                if array[0][q]==array[p][0]:
                    score_calc = (array[p-1][q-1]+matching_score),(array[p][q-1]+penalty),(array[p-1][q]+penalty)
                else:
                    score_calc = (array[p-1][q-1]-matching_score),(array[p][q-1]+penalty),(array[p-1][q]+penalty)
            else:
                score_calc = (-(row+1),array[p][q])
                
            array[p][q] = max(score_calc)
            maximum_index_list = []
            for i,calculation in enumerate(score_calc):
                if calculation == max(score_calc):
                    maximum_index_list.append(i) 
            backtrace_dict[p,q] = maximum_index_list
    df = pd.DataFrame(array)
    df.columns = df.iloc[0]
    a = list(df.columns)
    a[0] = "O"
    df.columns = a
    df.drop(0,inplace=True)
    df.to_csv("global_alignment_scoring_matrix.csv", index= False)
    return backtrace_dict, df, array



def backtracing(reference, query):
    "This function backtraces the score matrix using the backtrace_dict \
    and return the optimal alignment"
    list_ref = []
    list_query = []
    
    last_row = len(query)+1
    last_column = len(reference)+1
    
    backtrace_dict = scoring(reference,query)[0]
    
    while last_row > 1 or last_column > 1:
        if backtrace_dict[last_row,last_column] == [0]:
            list_ref.append(reference[last_column-2])
            list_query.append(query[last_row-2])
            last_row = last_row-1
            last_column = last_column-1
        elif backtrace_dict[last_row,last_column] == [1]:
            list_ref.append(reference[last_column-2])
            list_query.append("-")
            last_column=last_column-1
        else:
            list_query.append(query[last_row-2])
            list_ref.append("-")
            last_row=last_row-1
    
    aligned_sequences = pd.DataFrame([list_ref[::-1],list_query[::-1]])
    aligned_sequences.to_csv("aligned_sequence.csv", index=False)
    #print("-----------Global Alignment-----------")
    #print(aligned_sequences)
    ref_str = "".join(list_ref[::-1])
    query_str = "".join(list_query[::-1])
    return aligned_sequences, ref_str, query_str



    
"""________________________________________________UI Interphase_______________________________________________________________"""


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
    reference_input = tkinter.Entry(root,width = 20, borderwidth=0, font=("Arial", 24), bg = "white")
    reference_input.place(x=x_location+100, y = y_location-15)

    # reference_label=tkinter.Label(root, text="reference: ", font = ("Arial", 24, "bold"))
    # reference_label.place(x= 50, y=150 )
    return reference_input




reference_input = draw_entry_and_label(reference_x_location, reference_y_location, "Reference: ")
 #draw reference entry box
query_input = draw_entry_and_label(query_x_location, query_y_location, "Query: ")
matching_score_input = draw_entry_and_label(matching_score_x_location, matching_score_y_location, "Match Score: ")
penalty_input = draw_entry_and_label(penalty_x_location, penalty_y_location, "Penalty: ")



def submit():
    """This is the function to that calls the the N-W algorithm in the backend and 
    displays the result in the refreshed page of the application"""

    global matching_score
    global penalty
    penalty = int(penalty_input.get())
    matching_score = int(matching_score_input.get())
    print(type(matching_score))
    ##scoring(reference_input.get(), query_input.get())
    result = backtracing(reference_input.get(), query_input.get())
    #result_display()
    for widget in root.winfo_children():
        if widget.winfo_class() != "Canvas":
            widget.destroy()
    for canv_object in range(2,6,1):
        canv.delete(canv_object)
    canv_text_align = canv.create_text(300,250,font = ("Arial", 26, "bold"), fill= "white")
    canv.itemconfig(canv_text_align, text = "Alignment")
    canv_text_ref = canv.create_text(300,300,font = ("Arial", 24, "bold"), fill= "white")
    canv.itemconfig(canv_text_ref, text=result[1])
    canv_text_query = canv.create_text(300,330,font = ("Arial", 24, "bold"), fill= "white")
    canv.itemconfig(canv_text_query, text=result[2])

    """write a function that can allow app user to download the alignment reuslts as well the matrix scores 
    calclated using dynamic programming with backtracing function in the backend"""

    
    bt_download = tkinter.Button(text="Download \n result")
    bt_download.place(x=250, y = 370, bordermode="inside")  







bt = tkinter.Button(text="Submit", command=submit)
bt.place(x=270, y = penalty_y_location+50,bordermode="inside")



root.mainloop()
    



    
    
