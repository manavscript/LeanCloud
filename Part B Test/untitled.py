import csv

name = []
scores = []
my_list = []

with open('Student_marks_list.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for col in csvReader:
        name.append(col[0])
        scores.append(col[1:7])
        
for i in range(1, len(scores)): 
    for j in range(0, len(scores[0])):
        scores[i][j] = int(scores[i][j]) 
    
"""Linear Search Algorithm to find the greatest number and to return the toppers. This uses linear search twice. The first is for a 
2-d array hence the big O is O(n) if fixed number of subjects otherwise it approaches O(n^2) and the second is a linear search for a 1-d array.
Depending upon the conditions, if the number of subjects are variable then it is O(n^2) otherwise, the asymptotic notation is O(n)"""

def linearsearch(name, scores):
    sum = [0] * len(scores)
    for j in range(0, len(scores[0])):
        max_score_index = 1
        
        for i in range(1, len(scores)):
            sum[i] = sum[i] + scores[i][j]
            if (scores[i][j]>scores[max_score_index][j]):
                max_score_index = i
        print("Topper in", scores[0][j], "is", name[max_score_index])
        first = second = third = 0
    for k in range(len(sum)):
              if (sum[k]>=sum[first]):
                  third = second
                  second = first
                  first = k
              elif (sum[k]>=sum[second]):
                  third = second
                  second = k
              elif (sum[k]>sum[third]):
                  third = k
    print("Best students in the class are (", name[first], name[second], name[third], ")" )    

linearsearch(name, scores)