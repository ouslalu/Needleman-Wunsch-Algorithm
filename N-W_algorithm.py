import pandas as pd

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



def scoring():
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



def backtracing():
    "This function backtraces the score matrix using the backtrace_dict \
    and return the optimal alignment"
    list_ref = []
    list_query = []
    
    last_row = len(query)+1
    last_column = len(reference)+1
    
    backtrace_dict = scoring()[0]
    
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
    
    aligned_sequences = pd.DataFrame([list_ref,list_query])
    aligned_sequences.to_csv("aligned_sequence.csv", index=False)
    print("-----------Global Alignment-----------")
    print(aligned_sequences)
    return aligned_sequences



if __name__ == "__main__":
    query = input("Query sequence: ").upper()
    reference = input("Reference sequence: ").upper()
    penalty = int(input("Penalty: "))
    matching_score = int(input("Matching Score: "))
    backtracing()
    
    
    


    
    
