#Smith-Waterman algorithm implementation
#the local alignment is marked by some symbols: '|' for mathces, '*' for mismatches, and '-' for gaps
import numpy as np
import tkinter as tk
import math

#for the GUI
window = tk.Tk()
window.geometry("500x200")
window.title("Smith-Waterman algorithm")

#declaring string variables for storing inputs
seq1_var = tk.StringVar()      #first sequence to align
seq2_var = tk.StringVar()      #second sequence to align
match_var = tk.StringVar()     #match score 
mismatch_var = tk.StringVar()  #mismatch score
gap_o_var = tk.StringVar()     #gap opening penalty
gap_e_var = tk.StringVar()     #gap extension penalty

#creating a label for the input variables using widget Label
seq1_label = tk.Label(window, text = 'sequence 1', font=('calibre',10, 'bold'))
seq2_label = tk.Label(window, text = 'sequence 2', font = ('calibre',10,'bold'))
match_label = tk.Label(window, text = 'match score', font = ('calibre',10,'bold'))
mismatch_label = tk.Label(window, text = 'mismatch penalty', font = ('calibre',10,'bold'))
gap_o_label = tk.Label(window, text = 'gap opening penalty', font = ('calibre',10,'bold'))
gap_e_label = tk.Label(window, text = 'gap extension penalty', font = ('calibre',10,'bold'))
  
#creating an entry for input variables using widget Entry
seq1_entry = tk.Entry(window,textvariable = seq1_var, font=('calibre',10,'normal'))
seq2_entry = tk.Entry(window, textvariable = seq2_var, font = ('calibre',10,'normal'))
match_entry = tk.Entry(window, textvariable = match_var, font = ('calibre',10,'normal'))
mismatch_entry = tk.Entry(window, textvariable = mismatch_var, font = ('calibre',10,'normal'))
gap_o_entry = tk.Entry(window, textvariable = gap_o_var, font = ('calibre',10,'normal'))
gap_e_entry = tk.Entry(window, textvariable = gap_e_var, font = ('calibre',10,'normal'))

#defining a function that will get the input variables
def submit():
    seq1_var.get()
    seq2_var.get()
    match_var.get()
    mismatch_var.get()
    gap_o_var.get()  
    gap_e_var.get()

#creating a button using the widget Button that will call the Close function 
def Close(): 
    submit
    window.destroy()  
sub_btn = tk.Button(window, text = 'Done', command = Close)   
  
#placing label and entry in the wanted position using grid method
seq1_label.grid(row=0,column=0)
seq1_entry.grid(row=0,column=1)
seq2_label.grid(row=1,column=0)
seq2_entry.grid(row=1,column=1)
match_label.grid(row=2,column=0)
match_entry.grid(row=2,column=1)
mismatch_label.grid(row=3,column=0)
mismatch_entry.grid(row=3,column=1)
gap_o_label.grid(row=4,column=0)
gap_o_entry.grid(row=4,column=1)
gap_e_label.grid(row=5,column=0)
gap_e_entry.grid(row=5,column=1)
sub_btn.grid(row=6,column=1)
  
window.mainloop()  #performing an infinite loop for the window to display

s1 = seq1_var.get()     #taking the inputs through the function get()
s2 = seq2_var.get()          
match = int(match_var.get())
mismatch = int(mismatch_var.get())
gap_o = int(gap_o_var.get()) 
gap_e = int(gap_e_var.get()) 

len1 = len(s1)+1                       #number of rows of the matrix
len2 = len(s2)+1                       #number of columns of the matrix
table = np.zeros((len1, len2))         #creating the matrix to fill with the scores
table1 = np.full((len1, len2), '*')    #creating the matrix to fill with the directions for backtracking

def fill_matrix_sw(matrix, s1, s2, matrix1):     #filling matrices with scores (matrix) and backtracking information (matrix1)
    for i in range(1, matrix.shape[0]):          #number of rows
        for j in range(1, matrix.shape[1]):      #number of columns
            if s2[j-1] == s1[i-1]:               #there's a match
                score = matrix[i-1, j-1]+match   #score in case there's a match
                matrix1[i, j] = 'D'              #filling the matrix1 for backtracking
            if s2[j-1] != s1[i-1]:               #same but in case there's a mismatch
                score = matrix[i-1, j-1]+mismatch
                matrix1[i, j] = 'D'   
            if matrix1[i, j-1] == 'L' and matrix[i, j-1]+gap_e > score:     #we are dealing with a gap extension
                score = matrix[i, j-1]+gap_e  
                matrix1[i, j] = 'L' 
            if matrix1[i-1, j] == 'U' and matrix[i-1, j]+gap_e > score:     #we are dealing with a gap extension
                score = matrix[i-1, j]+gap_e  
                matrix1[i, j] = 'U' 
            if matrix1[i, j-1] == 'D' or matrix1[i, j-1] == 'U':             #we are dealing with a gap opening
                if matrix[i, j-1]+gap_o > score:
                    score = matrix[i, j-1]+gap_o 
                    matrix1[i, j] = 'L'
            if matrix1[i-1, j] == 'D' or matrix1[i-1, j] == 'L':            #we are dealing with a gap opening
                if matrix[i-1, j]+gap_o > score:
                    score = matrix[i-1, j]+gap_o 
                    matrix1[i, j] = 'U'
            matrix[i, j] = score                 #maximum value that was found for the score is recorded
            if score < 0:                        #scores under 0 are considered as 0
                matrix[i, j] = 0
    return matrix, matrix1

fill_matrix_sw(table, s1, s2, table1)

#going through all the cells and finding the one with the highest score
max_score = 0
for i in range(1, table.shape[0]):  
    for j in range(1, table.shape[1]):
        if table[i, j] > max_score:
            max_score = table[i, j]
            pos_i = i
            pos_j = j

min_score = math.ceil(max_score*0.8)   #all the alignments with a score higher or equal than 0.8*max_score are given in output
d_score_pos = {}                       #dictionary to store candidate scores and starting positions
for i in range(1, table.shape[0]):     #to find candidate scores and positions
    for j in range(1, table.shape[1]):
        if table[i, j] >= min_score:
            score = table[i, j]
            position = [[i,j]]
            if(score not in d_score_pos):    #a new key is created if not already present
                d_score_pos[score] = []
            d_score_pos[score] = d_score_pos[score] + position   #to handle the case in which more alignments have the same score
sorted_d = dict(sorted(d_score_pos.items(), reverse = True))     #sort in decreasing order. If this is not done, the overlapping problem is not solved 

dic = {}               #for later use (output printing)
overlap_list = []      #to keep track of the positions visited while backtracking
for value in sorted_d.values():   #iteration in the dictionary values (positions)
    current_score = list(d_score_pos.keys())[list(d_score_pos.values()).index(value)]  #score corresponding to the current position
    for el in value:
        if (el[0], el[1]) in overlap_list:  #we skip the alignment starting at el[0], el[1] since another alignment already passed there
            continue
        x = el[0]
        y = el[1]
        f1 = ''
        f2 = ''
        ngaps1 = 0
        ngaps2 = 0
        #backtracking
        while table[x, y] > 0:          #when a 0 comes, the local alignment stops
            z = (x,y)
            if z not in overlap_list:   #append to overlap_list all the positions visited during backtracking
                overlap_list.append(z)
            if table1[x, y] == 'D':     #'D' is found
                f2 = s2[y-1] + f2       #both f1 and f2 gain a character taken from the original strings s1 and s2
                f1 = s1[x-1] + f1
                x = x-1                 #both x and y decrease in order to move in diagonal
                y = y-1
            elif table1[x, y] == 'L':   #'L' is found
                f2 = s2[y-1] + f2       #only f2 gains a character, in f1 a gap is introduced
                f1 = '-' + f1                   
                y = y-1                 #only y decreases in order to move to the left
                ngaps1 += 1
            elif table1[x, y] == 'U':   #'U' is found
                f2 = '-' + f2           #only f1 gains a character, in f2 a gap is introduced
                f1 = s1[x-1] + f1
                x = x-1                 #only x decreases in order to move up
                ngaps2 += 1
        m = x    #memorizing these indices for later to complete the sequences
        n = y

        f3 = ''
        l = len(f1)

        #adding the "|" character where we find a match, '*' where we find a mismatch, and '-' where we find a gap in the final alignment
        nmatches = 0      #keeps track of the total number of matches
        nmismatches = 0   #keeps track of the total number of mismatches
        for i in range(l): 
            if f1[i] == f2[i]:
                f3 = f3 + '|'    #match
                nmatches += 1
            elif f1[i] == '-' or f2[i] == '-':
                f3 = f3 + '-'    #gap
            else:
                f3 = f3 + '*'    #mismatch
                nmismatches += 1

        #completing the two strings with the missing parts from the original strings s1 and s2 for proper visualization
        #note that these parts are not part of the local alignment
        #the local alignment is marked by the symbols '-' for gaps, '*' for mathces and '|' for mismatches
        #m, n is the position where the local alignment stopped at the end of backtracking; el[0], el[1] is where it started
        if m > n: 
            a1 = m-n
            f2 = a1*' ' + s2[:n] + f2 + s2[el[1]:]
            f1 = s1[:m] + f1 + s1[el[0]:]
            f3 = (a1+n)*' ' + f3
        else: 
            a2 = n-m
            f2 = s2[:n] + f2 + s2[el[1]:]
            f1 = a2*' ' + s1[:m] + f1 + s1[el[0]:]
            f3 = (a2+m)*' ' + f3

        l_a = nmatches + nmismatches + ngaps1 + ngaps2  #length of the local alignment

        #printing the output
        alignment = [(f1 + '\n' + f3 + '\n' + f2 + '\n' + 'local alignment length: ' + str(l_a) + '\n' + 'number of matches: ' 
                    + str(nmatches) + '\n' + 'number of mismatches: ' + str(nmismatches) + '\n' + 'number of gaps in sequence 1: ' + 
                    str(ngaps1) + '\n' + 'number of gaps in sequence 2: ' + str(ngaps2) + '\n')] #to concatenate all the info to output
        if(current_score not in dic):    #a new key is created if not already present
            dic[current_score] = []
        dic[current_score] = dic[current_score] + alignment   #to handle the case in which more alignments have the same score

sorted_dic = dict(sorted(dic.items(), reverse = True))  #sort in decreasing order
for key, el in sorted_dic.items():                      #print the output
    for item in el:
        print('score: ', key)
        print(item)