
import functions

" Reading an unsolved Sudoku from a CSV file called input.csv consisting of an unsolved Sudoku with 0’s representing blanks"

Test = open("input.csv", 'r')
text = Test.read()
grid = text.replace(',', '')
grid1 = grid.replace('\n', '')
Test.close()


# Solving Sudoku puzzle using Constraint Propagation algorithm
output = functions.display(functions.search(functions.parse_grid(grid1)))


# Convert the final result to CSV format
j = 1
list1 = ''
for i in output:
    if j % 9 != 0:
        list1 = list1 + i + ","
    elif j % 9 == 0:
        list1 = list1 + i + "\n"
    j += 1


# Saving the result in a CSV file called Result.csv
out = open("Result.csv", 'w')
out.write(list1)
out.close()
