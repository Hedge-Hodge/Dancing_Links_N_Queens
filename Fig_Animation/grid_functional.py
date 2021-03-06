import numpy as py
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
import warnings

warnings.filterwarnings("ignore")


# Specific NQueens function: Creates an empty matrix of size n^2 by 2(3n-3),
# to hold all possible placements and constraints
# Arguments: n = size of board
# Return: one_zero = Empty matrix
def create_one_zero_matrix(n):
    one_zero = py.zeros(((n ** 2), (2 * (3 * n - 3))), dtype=int)  # Native numpy function to create a zero matrix
    # See report for details about these dimensions
    return one_zero


# Specific NQueens function: Populates the one-zero matrix according to all possible queen placements
# Specific function for NQueens application
# Arguments: one_zero_matrix = empty 1-0 matrix created by 'create_one_zero_matrix', n = size of board
# Return: one_zero_matrix = matrix defining the exact cover problem
def populate_one_zero_matrix(one_zero_matrix, n):
    counter = 0
    # Iterate over the row indices, from (0,j) to (n,j)
    for i in range(n):
        # Set current x value
        x = i
        # Iterate over the column indices, from (i,0) to (i,n)
        for k in range(n):
            # print("Iterate, ", counter) DEBUG
            # Define an emtpy row, with length equal to the number of constraints
            current_row = []
            for p in range(2 * (3 * n - 3)):
                current_row.append(0)
            # Set current y value
            y = k
            # Compute the diagonal and backward diagonal constraints
            diag_constraint = (2 * n - 1) + x + y
            back_diag_constraint = 5 * n - 5 - x + y
            # Now populate the current row with 1's wherever constraints are satisfied
            current_row[x] = 1
            current_row[y + n] = 1
            # Check to see if this is a significant diagonal
            if (2 * n - 1) < diag_constraint < (4 * n - 3):
                current_row[diag_constraint] = 1
            # Check to see if this is a significant backward diagonal
            if (4 * n - 3) <= back_diag_constraint < (6 * n - 6):
                current_row[back_diag_constraint] = 1
            one_zero_matrix[counter] = current_row
            counter = counter + 1
    return one_zero_matrix


# Class declaration for the column headers
# No initial specification of the attributes
class Column:
    def __init__(self):
        self.left = None  # Points to the node/column header to the left of this header
        self.right = None  # Points to the node/column header to the right of this header
        self.up = None  # Points to the node above this header
        self.down = None  # Points to the node below this header
        self.size = 0  # Refers to the number of nodes below this object/ in it's column
        self.name = None  # Cosmetic attribute for outputting solutions
        self.primary = True  # Specific attribute for NQueens, see report for more details


# Class declaration for the regular nodes.
# These nodes will be used in the overall list object to represent 1's from the 1-0 matrix
# No initial specification of the attributes
class Node:
    def __init__(self):
        self.left = None  # Points to the node to the left
        self.right = None  # Points to the node to the right
        self.up = None  # Points to the node/column header above
        self.down = None  # Points to the node/column header below
        self.column = None  # Points to the column header above, regardless of how many nodes are above


# Class declaration for the overall list object.
# The master node/column header is specified initially,
# As well as the solution list and the total number of solutions
class CircularList:
    def __init__(self, master_node=Column()):
        self.colour2 = 'blue'
        self.master_node = master_node  # Create a column header to be the master node
        master_node.name = "Master"  # Set this header's name
        master_node.size = 10000000000000  # Set the master node's size to be very large,
        # so that it is never chosen to be part of the solution
        master_node.primary = False  # If this is a general application of DLX, this condition is needed for
        # solutions to be found. See self.dlx for details
        self.solution_list = []  # Used to store the nodes in the solution
        self.total_solutions = 0  # Used to count the number of solutions, for labelling their output later
        self.file_write_initial()  # Call the initial main file function
        self.file_write_initial_log()  # Call the initial log file
        self.header_list = []  # Stores the original order of header names, for outputting solutions
        self.move_set = []  # List of lists to keep track of move set
        self.current_move = []  # Temporary list of current move coordinates
        self.board = py.zeros((N, N))  # Initial board is an N X N zero matrix
        self.backtrack_counter = 0  # Counter for keeping track of backtracking
        self.colour_map = colors.ListedColormap(['yellow', 'green'])  # default colourscheme for grid

    # Helper function: Finds a named column's index
    # Starts at the master node
    # Arguments: name = The name of the column to search for
    # Return: The index of the column
    def find_column_index_by_name(self, name):
        current_node = self.master_node  # Start at index == 0
        index = 0
        # print("NAME", name) #DEBUG
        # Standard loop over column headers
        while current_node.name != name:
            # print(current_node.name) #DEBUG
            current_node = current_node.right  # Step right
            index = index + 1  # Increase index
        return index

    # Helper function: Finds a particular column header, given its index
    # Arguments: index = The index of the column to be found
    # Return: column object
    def find_column_by_index(self, index):
        current_column = self.master_node  # Start at the master node
        # Take number of steps right equal to the index
        for i in range(index):
            current_column = current_column.right  # Step right
        return current_column

    # Specific NQueens function: Transform the column headers to resemble the NQueens problem
    # Changes the names of the column headers according to n
    # Sets the column.primary attributes to false for the diagonal and back diagonal constraints
    # Calls the NQueen specific file write function, to record these changes for the user
    # Arguments: n = number of ranks/files of the board
    # Return: None
    def transform_n_queen(self, n):
        current_column = self.master_node
        # Iterate over all headers, using a for loop to easily track the index
        for i in range(2 * (3 * n - 3)):
            current_column = current_column.right  # Step right
            # Ranks
            if i < n:
                current_column.name = "Row {0}".format(i + 1)
            # Files
            elif i < 2 * n:
                current_column.name = "File {0}".format(int((i % n) + 1))
            # Diagonals
            elif i < (4 * n - 3):
                current_column.name = "Diagonal {0}".format(int((i % (2 * n)) + 1))
                current_column.primary = False
            # Back Diagonals
            else:
                current_column.name = "Back Diagonal {0}".format(int((i % (4 * n - 3)) + 1))
                current_column.primary = False
        self.file_write_n_queen(n)  # Write the according introduction to the main output file
        self.create_original_header_list()
        return None

    # Helper function: Updates the solution list by adding a new node
    # The list index is changed to the new node, or the new node is appended if the index is out of range
    # Arguments: new_node = the new node to be added to the solution
    # k = the depth of the DLX algorithm/ the index of the list to be updated
    # Return: None
    def set_solution_k(self, new_node, k):
        try:
            self.solution_list[k] = new_node  # Try to update index k
        except:
            self.solution_list.append(new_node)  # If out of range, append instead
        # Algorithm DLX will not 'skip' a k, ie. the index will never be more than one step out of range
        return None

    # Debug function: Prints all of the list object's column headers, along with their size,
    # to the standard console output.
    # Useful for monitoring the list throughout DLX
    # Arguments: None
    # Return: None
    def print(self):
        # current_header = self.master_node.right
        while current_header != self.master_node:
            # print(current_header.name, current_header.size)
            current_header = current_header.right
        return None

    # Debug function: Prints the solution list to the standard console output
    # Useful for monitoring the progress throughout DLX
    # Arguments: None
    # Return: None
    def print_solution(self):
        # print("Solution")
        for i in range(len(self.solution_list)):
            print(self.solution_list[i].column.name, self.solution_list[i].right.column.name)
        # Room for improvement here with a 'furthest left' function
        # print("End Solution")
        return None

    # Core function: Begins the main output file, also writing a small introduction
    # Arguments: None
    # Return: None
    def file_write_initial(self):
        # Use the write method here to overwrite any existing file contents
        solution_file = open("main_output.txt", "w")  # Open the file in write mode
        solution_file.write("Algorithm DLX\n\n")
        solution_file.write("This algorithm finds all solutions to an exact cover problem.\n")
        solution_file.write("An implementation of Donald Knuth's algorithm X, using dancing links, is used.\n")
        solution_file.write("For more information visit: https://github.com/Hedge-Hodge/Dancing_Links_N_Queens\n")
        solution_file.write("This file contains these solutions.\n")
        solution_file.close()  # Good practice to close files when finished
        return None

    # Specific Nqueens function: Add a brief NQueens specific description to the main output file
    # Arguments: n = the number of ranks/files of the chessboard
    # Return: None
    def file_write_n_queen(self, n):
        solution_file = open("main_output.txt", "a")  # Open the file in append mode
        solution_file.write("Here we have the classic N-Queens exact cover problem, with:\n")
        solution_file.write("N = {0}\n".format(n))
        solution_file.write("The columns of the matrix above correspond to the row, column and diagonal constraints.\n")
        solution_file.write("While the rows correspond to possible queen placements.\n")
        solution_file.close()
        return None

    # Helper function: Used to write the 1-0 matrix to the main output file, used in general and with NQueens
    # Arguments: martix = The numpy n dimension array holding the 1-0 matrix
    # Return: None
    def file_write_one_zero(self, matrix):
        solution_file = open("main_output.txt", "a")  # Open the file in append mode
        solution_file.write("\nThe following matrix represents the exact cover problem in question:\n")
        py.savetxt(solution_file, matrix, delimiter=' ', fmt='%i')  # Here the fmt argument writes only integers
        solution_file.close()
        return None

    # Helper function: Used to write a single solution to either output file
    # The filename is passed as an argument here allowing this to be used in both the main output and log files
    # Some bad practice here, with if statements. Open to suggestions.
    # Arguments: filename = either 'main_output.txt' or 'log_output.txt'
    # Return: None
    def file_write_solution(self, filename):
        # Only update the counter for the main output file, otherwise we would update twice for each solution
        if filename == "main_output.txt":
            self.total_solutions = self.total_solutions + 1
        # Open the file in append mode
        file = open(filename, "a")
        # If this is the first time writing a solution, include this header
        if self.total_solutions == 1:
            file.write("\n\nSolutions:\n\n")
        # This sub-header provides the solution number, equal to the total number of solutions at the time of writing
        file.write("Solution {0}\n".format(self.total_solutions))
        # Write the entire solution list to the file
        for i in range(len(self.solution_list)):
            # Furthest left nonsense is a relic of a failed optimization
            furthest_left = self.find_furthest_left(self.solution_list[i])
            # furthest_left = self.solution_list[i]
            # Write the node in the solution, as well as the node to the right of it
            file.write(furthest_left.column.name)
            file.write(", ")
            file.write(furthest_left.right.column.name)
            file.write("\n")
        file.write("\n")
        file.close()
        return None

    # Core function: Begins the log file, also writing a small introduction
    # Arguments: None
    # Return: None
    def file_write_initial_log(self):
        log_file = open("log_output.txt", "w")
        log_file.write("DLX Log\n\n")
        log_file.write("See 'main_output.txt' for the proper algorithm output and aesthetic solution list.\n")
        log_file.write("This file contains a detailed record of each iteration of the recursive DLX algorithm.\n")
        log_file.write("Each time a new row is chosen, this will be logged here.\n")
        log_file.write("Each time the algorithm finds itself in a 'dead end' (i.e. when some of the remaining "
                       "constraints have size=0) this will be recorded also.\n\n\n")
        log_file.write("Begin log:\n")
        log_file.close()
        return None

    # Helper function: Finds a column header's original index, regardless of any current covered columns.
    # This function facilitates the find_furthest_left function, to ensure rows of the solution always start with the
    # furthest left node.
    # Arguments: name = the name of the column to be searched for
    # Return: index = the column header's original index.
    # Note this can also return None, if no match was found for the inputted name.
    def find_original_index_by_name(self, name):
        index = 0
        for i in range(len(self.header_list)):
            if name == self.header_list[i]:
                return index
            index = index + 1
        #print("DEBUG: No matching name found in the original column header list.")
        return None

    # Helper function: Initialises the header list, used to ensure the order in which nodes in the solution are written
    # to file, is correct. This MUST be called each time the column header's names change.
    # Arguments: None
    # Return: None
    def create_original_header_list(self):
        current_header = self.master_node.right
        while current_header != self.master_node:
            self.header_list.append(current_header.name)
            current_header = current_header.right
        return None

    # Helper function: Finds the furthest left node in a row. Used to ensure the order in which nodes in the solution
    # are written to file are correct.
    # Arguments: current_node = a node in the row to be searched
    # Return: best_node = the furthest left node
    def find_furthest_left(self, current_node):
        dummy_node = current_node.left
        best_node = current_node
        # print("current node", current_node)
        best_index = self.find_original_index_by_name(current_node.column.name)
        # print("best index", best_index)
        while dummy_node != current_node:
            dummy_index = self.find_original_index_by_name(dummy_node.column.name)
            # print("dummy", dummy_index)
            if dummy_index < best_index:
                best_node = dummy_node
                best_index = dummy_index
            dummy_node = dummy_node.left
        return best_node

    # Core function: Write a single iteration of DLX to the log
    # This write will include the depth of the algorithm as well as the row it has chosen to try.
    # This will also record a BACKTRACK in the log, depending on the backtrack argument
    # Arguments: node = the node/row to be recorded
    # k = the depth of the algorithm at this time, default = 0
    # backtrack[boolean] = whether or not to record a backtrack in the log, default = False
    # Return: None
    def log_row_board(self, node, k=0, backtrack=False):
        self.current_move = []  # list of current moves, namely row = X and file = Y
        log_file = open("log_output2.txt", "a")
        if backtrack:
            self.backtrack_counter += 1  # counter that tells us to delete some previous nodes
            log_file.write("Problem encountered,\t")
            log_file.write(node.name)
            log_file.write("\tis a dead constraint. BACKTRACK.\n")
        else:
            current_node = self.find_furthest_left(node)
            # Write the current depth of the algorithm
            log_file.write("k={0}\n".format(k))
            # Simple placeholder
            log_file.write("Row:\t")
            log_file.write(current_node.column.name)
            self.current_move.append(current_node.column.name)
            dummy_node = current_node.right
            # Iterate across the row, writing the name of the node's column header each time
            self.current_move.append(dummy_node.column.name)
            while dummy_node != current_node:
                log_file.write("\t")
                dummy_node = dummy_node.right
            log_file.write("\n")
        log_file.close()
        self.move_set.append(self.current_move)  # add current move to move set list
        moves_df = pd.DataFrame(self.move_set)  # convert move set list to pandas dataframe
        moves_df[0] = moves_df[0].str.replace("Row ", "")  # remove strings
        moves_df[1] = moves_df[1].str.replace("File ", "")
        moves_df.dropna(inplace=True)  # remove NaN data that appears due to how backtracking is handled
        New_move = int(moves_df[0].iloc[-1])  # new move's row
        if self.backtrack_counter == 1:
            self.backtrack_counter += 1
            self.colour2 = 'red'  # use the red backtrack board on grid
        elif self.backtrack_counter == 2:  # backtrack before new move is added
            self.backtrack_counter -= 2
            for i in range(N):
                for j in range(New_move - 1, N):
                    self.board[(j, i)] *= 0  # Delete all rows below the new move to backtrack
            self.board[
                (int(moves_df[0].iloc[-1]) - 1), (int(moves_df[1].iloc[-1]) - 1)] += 1  # Add new move to the 4X4 matrix
            self.colour2 = "blue"  # new moves get blue colour scheme
        else:  # if no backtracking, add new move
            for i in range(N):
                self.board[New_move - 1, i] = 0  # clear any other moves in row
            self.board[(int(moves_df[0].iloc[-1]) - 1), (int(moves_df[1].iloc[-1]) - 1)] += 1  # if no backtracking,
            self.colour2 = "blue"
        chessboard_figure(N, self.colour2, 0.1, self.board)
        if self.board.sum() == N:  # solution is found when there is N correct placements on the board
            print("Solution", self.total_solutions + 1, "Found!")
            chessboard_figure(N, "green", 1, self.board)  # Green colour scheme for success!
            self.backtrack_counter = 2
            self.move_set = []  # resets moves list
        return None

    # Core function: This very important function converts a 1-0 matrix into a general list object
    # No checks are performed to see if the problem is well defined
    # The column headers are given default names in the format: "constraint {i}" from 0, number of constraints
    # This function has three sections:
    #   1.) Create the column headers
    #   2.) Create the rows
    #   3.) Join any loose ends on the left/right of rows, and top/bottom of columns
    # Arguments: matrix = the 1-0 matrix to be converted
    # Return: master_node = the master node of the list object, so its pointer can be stored elsewhere outside
    # these methods
    def convert_one_zero(self, matrix):
        self.file_write_one_zero(matrix)  # First record the matrix in the main output file
        dims = py.shape(matrix)  # Find the dimensions of the matrix
        x = dims[0]  # Number of rows
        y = dims[1]  # Number of columns

        # Create the column headers
        previous_header = self.master_node
        for i in range(y):
            new = Column()  # Initialise new column header
            new.name = "Constraint {0}".format(i)  # Generic name
            # Connect to the previous header on the left
            new.left = previous_header
            previous_header.right = new
            # Connect on the right to the master node.
            # Note: These next two will be overwritten for each iteration i, except the last
            new.right = self.master_node
            self.master_node.left = new
            # Update pointer for next iteration
            previous_header = new

        # Create each row
        for i in range(x):
            # Extract corresponding row from 1-0 Matrix
            current_row = matrix[i]
            first_pass = True  # Bad practice, can't think of a better solution right now. Need to operate differently
            # if this is the first node in the row.

            # Iterate over the extracted row
            for j in range(y):
                # If significant, we only record 1s from the 1-0 matrix of course
                if current_row[j] == 1:
                    new = Node()  # Create new node
                    new.column = self.find_column_by_index(j + 1)  # Define column header for new node
                    current_above = new.column
                    # Find 'lowest' node in the column
                    while current_above.down is not None:
                        current_above = current_above.down
                    # Connect new.up to current_above.down
                    current_above.down = new
                    new.up = current_above
                    # If this is the first node, no previous node declared and no left connection available
                    if first_pass:
                        first_node = new
                        first_node.left = first_node
                        first_node.right = first_node
                        prev_node = first_node  # Record this node for the next iteration
                        first_pass = False
                    else:
                        # Connect new node on the left to the previous node in this row
                        new.left = prev_node
                        prev_node.right = new
                        new.right = first_node
                        first_node.left = new
                        prev_node = new
        # Finally join the edges of the lists
        # Start at the master node
        current_header = self.master_node.right  # Current header will be used to traverse the chain horizontally
        # Iterate right until we are at the last node
        while current_header != self.master_node:
            current_node = current_header  # Current node will be used to traverse the chain vertically
            # Iterate down until we are at the 'lowest' node
            while current_node.down is not None:
                current_header.size = current_header.size + 1  # Update the size of this column for each step down
                current_node = current_node.down  # Step down
            # Join the 'lowest' node and the header, above and below
            current_node.down = current_header
            current_header.up = current_node
            current_header = current_header.right  # Step right
        self.create_original_header_list()  # This function is called now that the list object has no 'loose' edges
        # It is needed to facilitate the logging of solutions
        print(self.header_list)
        return self.master_node

    # DLX helper function: Cover a column of the list object
    # This is a complete copy of Donald Knuth's implementation in his paper(I hope)
    # Arguments: column = the column to be covered
    # Return: None
    def cover_column(self, column):
        # print("cover Column ", column.name) DEBUG
        # Remove column header from the header chain
        column.left.right = column.right  # Alter link to the left
        column.right.left = column.left  # Alter link to the right
        # Iterate down through the column
        current_node = column.down
        while current_node != column:
            # Iterate right across the row
            current_right = current_node.right
            while current_right != current_node:
                current_below = current_right.down  # Need to specify a temporary pointer to the node below & below
                current_above = current_right.up
                current_below.up = current_above  # Alter link below
                current_above.down = current_below  # Alter link above
                current_right.column.size = current_right.column.size - 1  # Alter column size
                current_right = current_right.right  # Step right
            current_node = current_node.down  # Step down
        return None

    # DLX helper function: Uncover a column of the list object
    # This is a complete copy of Donald Knuth's implementation in his paper(I hope)
    # This is the inverse of the cover_column function, all operations are reversed and done in the opposite order
    # Arguments: column = the column to be uncovered
    # Return: None
    def uncover_column(self, column):
        # print("Uncover Column ", column.name) DEBUG
        current_node = column.up
        while current_node != column:
            current_left = current_node.left
            while current_left != current_node:
                # print("Column", current_left.column.name, current_left.column.size)
                current_left.column.size = current_left.column.size + 1
                current_below = current_left.down
                current_above = current_left.up
                current_below.up = current_left  # Restore link below
                current_above.down = current_left  # Restore link above
                current_left = current_left.left  # Step left
            current_node = current_node.up  # Step up
        # Add column to the header chain
        column.left.right = column
        column.right.left = column
        return None

    # DLX helper function: Find the column with the smallest size to cover
    # By choosing the column with the smallest size, we limit the branching factor of the algorithm and increase it's
    # speed.
    # Arguments: None
    # Return: None
    def find_best_column(self):
        current_header = self.master_node.right
        best_header = self.master_node
        while current_header != self.master_node:
            # We only want to choose primary headers, there should only be non-primary headers in the NQueen application
            if current_header.size < best_header.size and current_header.primary:
                best_header = current_header
            current_header = current_header.right
        return best_header

    # DLX helper function: Check to see if the current list object has an columns of size=0, if it does the constraint
    # is dead. In this case a backtrack is necessary.
    # Arguments: None
    # Return: None
    def dead_constraint(self):
        current_header = self.master_node.right
        while current_header != self.master_node:
            # We do not care is non-primary constraints are dead
            if current_header.primary and current_header.size <= 0:
                self.log_row_board(current_header, backtrack=True)  # Log this backtrack
                return True
            current_header = current_header.right
        return False

    # Main DLX function: This is where we lose ourselves to dance(Daft Punk).
    # This calls many of the methods above.
    # This is a recursive function, see report for more details
    # Arguments: k = depth of the algorithm
    # Return: None
    def dlx(self, k):
        print("Starting algorithm DLX. k=", k)  # DEBUG
        # self.print()  # DEBUG
        # self.print_solution()  # DEBUG
        # If the only constraints left are non-primary ones, we have found a solution!
        if not self.master_node.right.primary:
            print("O frabjous day! Callooh! Callay!")  # DEBUG
            self.print_solution()  # DEBUG
            # Write this solution to both output files
            self.file_write_solution("main_output.txt")
            self.file_write_solution("log_output.txt")
            # Return now
            return None
        else:
            # Check to see if there are any dead constraints
            if self.dead_constraint():
                print("Dead constraint, need to backtrack")  # DEBUG
                # Return as the problem is not well defined anymore
                return None
            # Choose the column with the smallest size, by calling the find_best_constraint function
            current_column = self.find_best_column()
            # Best column now found
            print("Best column found, ", current_column.name)  # DEBUG
            # Branch now for each row in this column
            current_node = current_column.down  # Start below the column header, iterate down from here
            self.cover_column(current_column)  # First cover this column
            while current_node != current_column:
                self.set_solution_k(current_node, k)  # Add this to the solution list, will be overwritten if not a
                # solution.
                # Record this step of the algorithm in the log
                self.log_row_board(current_node, k, backtrack=False)
                # Iterate across this row
                current_right = current_node.right
                while current_right != current_node:
                    # Cover the column this node belongs to
                    self.cover_column(current_right.column)
                    current_right = current_right.right  # step right
                # print("Recursive call")  # DEBUG
                # Call dlx again, with depth += 1
                self.dlx(k + 1)
                current_node = self.solution_list[k]  # Retrieve the current node from the solution list
                current_column = current_node.column  # Find its column
                # Iterate left to uncover
                current_left = current_node.left
                while current_left != current_node:
                    # Uncover column of current node
                    self.uncover_column(current_left.column)
                    current_left = current_left.left  # step left
                current_node = current_node.down  # Step down
            self.uncover_column(current_column)  # Uncover the column originally chosen as best
        return None


N = 8


def chessboard_figure(N, colour2, pause_length, board):
    numbers = py.array(py.arange(N))  # make an array of [1,2...N] numbers
    fig1 = plt.figure(num="Chessboard", figsize=(N, N))  # used to make sure plots stays in the same window
    ax = fig1.add_subplot(111)
    colour_map = colors.ListedColormap(['white', colour2])  # colours of the board
    plt.pcolor(board[::-1], cmap=colour_map, edgecolors='k', linewidths=3)
    ax.set_xticklabels(numbers + 1)
    ax.set_yticklabels(py.flip(numbers + 1))
    ax.tick_params(axis=u'both', which=u'both', length=0)  # hide black tick lines
    plt.ylabel('Rank', fontsize=15)
    plt.xlabel('File', fontsize=15)
    plt.xticks(numbers + 0.5)  # ticks between boxes in grid
    plt.yticks(numbers + 0.5)
    fig1.canvas.draw_idle()
    plt.pause(pause_length)  # pause so we can see the move
    plt.cla()  # clears axis labels when finished.


chessboard_figure(N, "blue", 3, py.zeros((N, N)))

print("N = ", N)
print("Creating empty 1-0 Matrix...")
current_matrix = create_one_zero_matrix(N)
print("Done.")
# print(current_matrix)
print("Populating 1-0 Matrix...")
populate_one_zero_matrix(current_matrix, N)
print("Done.")
# print(py.shape(current_matrix))
# print(current_matrix)

# TESTS
test = CircularList()
test.convert_one_zero(current_matrix)
test.transform_n_queen(N)
this_node = test.master_node.right
while this_node != test.master_node:
    below = this_node.down
    # print(this_node.name)
    while below != this_node:
        counter = 0
        right = below.right
        while right != below:
            counter = counter + 1
            right = right.right
        # print(below, "Counter:", counter)
        below = below.down
    this_node = this_node.right

# PRAY
test.dlx(0)
