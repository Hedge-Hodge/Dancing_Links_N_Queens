# Imports
import numpy as np
import time

def user_interface():
    print("Welcome to DLX\n",
          "This algorithm solves an exact cover problem of your choice.\n")
    choice = 'Z'
    while choice != 'A' and choice != 'B':
        print("Please input the letter of your choice: 'A' or 'B'\n",
          "A.) Solve the N-Queens problem\n",
          "B.) Import your favourite matrix to solve (you will need the path/filename of this matrix)")
        choice = input("Answer: ").upper()
        if choice == 'A':
            print("You have chosen option A: \t Solve the N Queens problem.\n Please now specify N.")
            n = int(input("N = "))
            log_decision = 'Z'
            while log_decision != 'Y' and log_decision != 'N':
                print("Would you like an extensive log of all steps taken? (Will increase execution time of DLX)\n",
                      "Please answer: (Y/N)")
                log_decision = input().upper()
            if log_decision:
                begin_dlx_n_queen(n, True)
            else:
                begin_dlx_n_queen(n, False)
            return None
        elif choice == 'B':
            print("You have chosen option B:\t Solve your favourite matrix.")
            delimiter_type = 'Z'
            while delimiter_type != 'A' and delimiter_type != 'B':
                print("Please now specify if the values in your file are separated by:\nA.) commas \nB.) whitespace")
                delimiter_type = input("Answer: ").upper()
            print("Please now input the filename with path, including the extension, that holds the your favourite matrix.",
                  "\nFor example: user/project/dlx/input.csv")
            print("If the file is in the same directory as I am, no need to input the path.")
            filename = input("Filename (and path): ")
            try:
                if delimiter_type == 'A':
                    input_matrix = py.loadtxt(filename, dtype = int, delimiter=',')
                    print(input_matrix)
                elif delimiter_type == 'B':
                    input_matrix = py.loadtxt(filename, dtype=int)
                    print(input_matrix)
                log_decision = 'Z'
                while log_decision != 'Y' and log_decision != 'N':
                    print("Would you like an extensive log of all steps taken? (Will increase execution time of DLX)\n",
                          "Please answer: (Y/N)")
                    log_decision = input().upper()
                if log_decision:
                    begin_dlx_user_input_matrix(input_matrix, True)
                else:
                    begin_dlx_user_input_matrix(input_matrix, False)
                return None
            except:
                print("Error: Could not open file, please try again")
                return None
            return None

# Specific NQueens function: Creates an empty matrix of size n^2 by 2(3n-3),
# to hold all possible placements and constraints.
# See report for details about these dimensions.
# Arguments: n = size of board
# Return: one_zero = Empty matrix
def create_one_zero_matrix(n):
    one_zero = np.zeros(((n**2), (2*(3*n-3))), dtype=int)
    return one_zero


# Specific NQueens function: Populates the one-zero matrix according to all possible queen placements
# Arguments: one_zero_matrix = empty 1-0 matrix created by 'create_one_zero_matrix', n = size of board
# Return: one_zero_matrix = matrix defining the exact cover problem
def populate_one_zero_matrix(one_zero_matrix, n):
    counter = 0
    # Iterate over the row indices, from (0,j) to (n,j)
    for i in range(n):
        x = i
        # Iterate over the column indices, from (i,0) to (i,n)
        for k in range(n):
            current_row = []    # Define an emtpy row, with length equal to the number of constraints
            for p in range(2 * (3 * n - 3)):
                current_row.append(0)
            y = k
            # Compute the diagonal and backward diagonal constraints
            diag_constraint = (2*n - 1) + x + y
            back_diag_constraint = 5*n - 5 - x + y
            # Now populate the current row with 1's wherever constraints are satisfied
            current_row[x] = 1
            current_row[y + n] = 1
            # Check to see if this is a significant diagonal
            if (2 * n - 1) < diag_constraint < (4*n - 3):
                current_row[diag_constraint] = 1
            # Check to see if this is a significant backward diagonal
            if (4*n - 3) <= back_diag_constraint < (6*n - 6):
                current_row[back_diag_constraint] = 1
            one_zero_matrix[counter] = current_row
            counter = counter + 1
    return one_zero_matrix

# Class declaration for the regular nodes.
# All attributes initialised to 'None' by default
class Node:
    def __init__(self, left=None, right=None, up=None, down=None, column=None):
        self.left = left        # Points to the (node/column header) to the left of this object
        self.right = right      # Points to the (node/column header) to the right of this object
        self.up = up            # Points to the (node/column header) above this object
        self.down = down        # Points to the (node/column header) below this object
        self.column = column    # Points to the column header of the column this object belongs to


# Class declaration for the column headers
# All attributes initialised to 'None' or '0' by default, except primary attribute set to 'True'
class Column:
    def __init__(self, left=None, right=None, up=None, down=None, size=0, name=None, primary=True):
        self.left = left        # Points to the (node/column header) to the left of this object
        self.right = right      # Points to the (node/column header) to the right of this object
        self.up = up            # Points to the (node/column header) above this object
        self.down = down        # Points to the (node/column header) below this object
        self.size = size        # Refers to the number of nodes in this object's column (below)
        self.name = name        # Cosmetic attribute for outputting solutions
        self.primary = primary  # If set to 'False' object cannot be chosen by DLX and can be unsatisfied for solutions


# Class declaration for the overall list object.
# The master header is specified initially and its attributes are defined accordingly.
# The solution_list/total_solutions variables are initialised.
# The main and log file names are stored as attributes of this object.
class FourWayLinkedList:
    def __init__(self, main_file_name="main_output.txt", log_file_name="log.txt", master_node=Column(name="Master",primary=False)):
        self.main_file = main_file_name     # Store name of MAIN file for access later
        self.log_file = log_file_name       # Store name of LOG file for access later
        self.master_node = master_node      # Create a column header to be the master node
        self.solution_list = []             # Used to store the nodes in the solution
        self.total_solutions = 0            # Used to count the number of solutions, for labelling their output later
        self.header_list = []               # Stores the original order of header names, for outputting solutions

    # Helper function: Finds a named column's index
    # Starts at the master node
    # Arguments: name = The name of the column to search for
    # Return: The index of the column
    def find_column_index_by_name(self, name):
        current_node = self.master_node
        index = 0
        while current_node.name != name:
            current_node = current_node.right  # Step right
            index = index + 1  # Increase index
        return index

    # Helper function: Finds a particular column header, given its index
    # Arguments: index = The index of the column to be found
    # Return: column object
    def find_column_by_index(self, index):
        current_column = self.master_node
        # Take number of steps right equal to the index
        for i in range(index):
            current_column = current_column.right  # Step right
        return current_column

    # Specific N-Queens function: Transform the column headers to resemble the N-Queens problem.
    # Changes the names of the column headers according to n.
    # Sets the column.primary attributes to false for the diagonal and back diagonal constraints.
    # Calls the NQueen specific file write function, to record these changes for the user.
    # Arguments: n = number of ranks/files of the board
    # Return: None
    def transform_n_queen(self, n):
        current_column = self.master_node
        # Iterate over all headers, using a for loop to easily track the index
        for i in range(2 * (3 * n - 3)):
            current_column = current_column.right  # Step right
            if i < n:   # Ranks
                current_column.name = "Rank {0}".format(i + 1)
            elif i < 2*n:   # Files
                current_column.name = "File {0}".format(int((i % n) + 1))
            elif i < (4*n - 3): # Diagonals
                current_column.name = "Diagonal {0}".format(int((i % (2*n)) + 1))
                current_column.primary = False
            else:   # Back Diagonals
                current_column.name = "Back Diagonal {0}".format(int((i % (4*n - 3)) + 1))
                current_column.primary = False
        self.file_write_n_queen(n)  # Write the according introduction to the main output file
        self.create_original_header_list()  # Needs to be called again here as the column header's names have changed
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

    # Debug function: Prints all of the four way linked list object's column headers, along with their size,
    # to the standard console output.
    # Useful for monitoring the list throughout DLX
    # Arguments: None
    # Return: None
    def print(self):
        current_header = self.master_node.right
        while current_header != self.master_node:
            print(current_header.name, current_header.size)
            current_header = current_header.right
        return None

    # Debug function: Prints the solution list to the standard console output
    # Useful for monitoring the progress throughout DLX
    # Arguments: None
    # Return: None
    def print_solution(self):
        print("Solution")
        for i in range(len(self.solution_list)):
            print(self.solution_list[i].column.name, self.solution_list[i].right.column.name)
        print("End Solution")
        return None

    # File function: Calls the appropriate functions to initialise the output ad log files.
    # Arguments: log = boolean value specifying if the user desires an extensive log
    # Return: None
    def begin_file_writing(self, log):
        self.main_file_initial()
        if log:
            self.log_file_initial()
        return None

    # File function: Begins the main output file, also writing a small introduction
    # Arguments: None
    # Return: None
    def main_file_initial(self):
        # Use the write method here to overwrite any existing file contents
        solution_file = open(self.main_file, "w")  # Open the file in write mode
        solution_file.write("Algorithm DLX\n\n")
        solution_file.write("This algorithm finds all solutions to an exact cover problem.\n")
        solution_file.write("An implementation of Donald Knuth's algorithm X, using dancing links, is used.\n")
        solution_file.write("For more information visit: https://github.com/Hedge-Hodge/Dancing_Links_N_Queens\n")
        solution_file.write("This file contains these solutions.\n")
        solution_file.close()  # Good practice to close files when finished
        return None

    # File function: Begins the log file, also writing a small introduction
    # Arguments: None
    # Return: None
    def log_file_initial(self):
        log_file = open(self.log_file, "w")
        log_file.write("DLX Log\n\n")
        log_file.write("See '{0}' for the proper algorithm output and aesthetic solution list.\n".format(self.main_file))
        log_file.write("This file contains a detailed record of each iteration of the recursive DLX algorithm.\n")
        log_file.write("Each time a new row is chosen, this will be logged here.\n")
        log_file.write("Each time the algorithm finds itself in a 'dead end' (i.e. when some of the remaining "
                       "constraints have size=0) this will be recorded also.\n\n\n")
        log_file.write("Begin log:\n")
        log_file.close()
        return None

    # N-Queens/File function: Add a brief NQueens specific description to the main output file
    # Arguments: N = the number of ranks/files of the chessboard
    # Return: None
    def file_write_n_queen(self, N):
        solution_file = open(self.main_file, "a")  # Open the file in append mode
        solution_file.write("Here we have the classic N-Queens exact cover problem, with:\n")
        solution_file.write("N = {0}\n".format(N))
        solution_file.write("The columns of the matrix above correspond to the row, column and diagonal constraints.\n")
        solution_file.write("While the rows correspond to possible queen placements.\n")
        solution_file.close()
        return None

    # File function: Used to write the 1-0 matrix to the main output file, used in general and with NQueens
    # Arguments: matrix = The numpy n dimension array holding the 1-0 matrix
    # Return: None
    def file_write_one_zero(self, matrix):
        solution_file = open(self.main_file, "a")  # Open the file in append mode
        solution_file.write("\nThe following matrix represents the exact cover problem in question:\n")
        np.savetxt(solution_file, matrix, delimiter=' ', fmt='%i')  # Here the fmt argument writes only integers
        solution_file.close()
        return None

    # File function: Write a single iteration of DLX to the log
    # This write will include the depth of the algorithm as well as the row it has chosen to try.
    # This will also record a BACKTRACK in the log, depending on the backtrack argument
    # Arguments: node = the node/row to be recorded
    # k = the depth of the algorithm at this time, default = 0
    # backtrack[boolean] = whether or not to record a backtrack in the log, default = False
    # Return: None
    def file_write_log_row(self, node, k=0, backtrack=False):
        log_file = open(self.log_file, "a")
        # If the algorithm is in a 'dead-end' record a backtrack in the log
        if backtrack:
            log_file.write("BACKTRACK necessary,\t")
            log_file.write(node.name)
            log_file.write("\tis a dead constraint.\n")
        # Otherwise write this row into the solution
        else:
            current_node = self.find_furthest_left(node)
            #current_node = node
            # Write the current depth of the algorithm
            log_file.write("k={0}\n".format(k))
            # Simple placeholder
            #log_file.write("Rank:\t")
            log_file.write(current_node.column.name)
            dummy_node = current_node.right
            # Iterate across the row, writing the name of the node's column header each time
            while dummy_node != current_node:
                log_file.write("\t")
                log_file.write(dummy_node.column.name)
                dummy_node = dummy_node.right
            log_file.write("\n")
        log_file.close()
        return None

    # File function: Used to write a single solution to either output file
    # The filename is passed as an argument here allowing this to be used in both the main output and log files
    # Some bad practice here, with if statements. Open to suggestions.
    # Arguments: main_file = boolean value, true for the main file, false for the log file
    # Return: None
    def file_write_solution(self, main_file=True):
        # Only update the counter for the main output file, otherwise we would update twice for each solution
        if main_file:
            self.total_solutions = self.total_solutions + 1
            file = open(self.main_file, "a")
        else:
            file = open(self.log_file, "a")
        # If this is the first time writing a solution, include this header
        if self.total_solutions == 1:
            file.write("\n\nSolutions:\n\n")
        # This sub-header provides the solution number, equal to the total number of solutions at the time of writing
        file.write("Solution {0}\n".format(self.total_solutions))
        # Write the entire solution list to the file
        for i in range(len(self.solution_list)):
            furthest_left = self.find_furthest_left(self.solution_list[i])
            # Write the node in the solution, as well as the node to the right of it
            file.write(furthest_left.column.name)
            file.write(", ")
            file.write(furthest_left.right.column.name)
            file.write("\n")
        file.write("\n")
        file.close()
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
        print("Warning: No matching name found in the original column header list.")
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
        dummy_node, best_node = current_node.left, current_node
        #best_node = current_node
        best_index = self.find_original_index_by_name(current_node.column.name)
        while dummy_node != current_node:
            dummy_index = self.find_original_index_by_name(dummy_node.column.name)
            if dummy_index < best_index:
                best_node, best_index = dummy_node, dummy_index
                #best_index = dummy_index
            dummy_node = dummy_node.left
        return best_node


    # Core function: This very important function converts a exact cover matrix into a general list object
    # No checks are performed to see if the problem is well defined
    # The column headers are given default names in the format: "constraint {i}" from 0, number of constraints
    # This function has three sections:
    #   1.) Create the column headers
    #   2.) Create the rows
    #   3.) Join any loose ends on the left/right of rows, and top/bottom of columns
    # Arguments: matrix = the 1-0 matrix to be converted
    # Return: master_node = the master node of the list object, so its pointer can be stored elsewhere outside
    # these methods
    def convert_exact_cover(self, matrix, log):
        self.begin_file_writing(log)
        self.file_write_one_zero(matrix)  # First record the matrix in the main output file
        dims = np.shape(matrix)  # Find the dimensions of the matrix
        x, y = dims  # Number of rows, number of columns
        # Create the column headers
        previous_header = self.master_node
        for i in range(y):
            new = Column(left=previous_header, right=self.master_node, name="Constraint {0}".format(i))  # Initialise new column header
            new.up, new.down = new, new
            previous_header.right = new
            self.master_node.left = new
            previous_header = new   # Update pointer for next iteration
        # Create each row
        for i in range(x):
            current_row = matrix[i]     # Extract corresponding row from 1-0 Matrix
            # Iterate over the extracted row
            prev_node = None
            for j in range(len(current_row)):
                current_node = Node()
                current_node.left, current_node.right = current_node, current_node
                if current_row[j] == 1:         # If significant, as we only record 1s from the 1-0 matrix
                    if prev_node is not None:
                        current_node.right, prev_node.right.left = prev_node.right, current_node
                        current_node.left, prev_node.right = prev_node, current_node
                    current_node.column = self.find_column_by_index(j + 1)          # Define column header for new node
                    current_node.column.size = current_node.column.size + 1
                    current_above = current_node.column
                    while current_above.down != current_node.column:            # Find 'lowest' node in the column
                        current_above = current_above.down
                    current_above.down, current_node.column.up = current_node, current_node
                    current_node.up, current_node.down = current_above, current_node.column
                    prev_node = current_node
        return self.master_node

    # DLX helper function: Cover a column of the list object
    # Implemented as directly as possible from Dancing Links paper by Knuth.
    # Alters the links around a column header, and around the nodes in each row of a column such that they are removed
    # from the list.
    # Arguments: column = the column header of the column to be covered
    # Return: None
    def cover_column(self, column):
        # Remove column header from the header chain
        column.left.right = column.right  # Alter link to the left
        column.right.left = column.left  # Alter link to the right
        # Iterate down through the column
        current_down = column.down
        while current_down != column:
            # Iterate right across the row
            current_right = current_down.right
            while current_right != current_down:
                current_right.down.up = current_right.up  # Alter link below
                current_right.up.down = current_right.down  # Alter link above
                current_right.column.size = current_right.column.size - 1  # Alter column size
                current_right = current_right.right  # Step right
            current_down = current_down.down  # Step down
        return None

    # DLX helper function: Uncover a column of the list object
    # Implemented as directly as possible from Dancing Links paper by Knuth.
    # Alters the links around a covered column header, and around the nodes in each row of a column such that they are restored
    # to the list.
    # This is the inverse of the cover_column method, notice that all operations are reversed and done in the opposite order
    # Arguments: column = the column header of the column to be uncovered
    # Return: None
    def uncover_column(self, column):
        current_up = column.up
        while current_up != column:
            current_left = current_up.left
            while current_left != current_up:
                current_left.column.size = current_left.column.size + 1
                current_left.down.up = current_left  # Restore link below
                current_left.up.down = current_left  # Restore link above
                current_left = current_left.left  # Step left
            current_up = current_up.up  # Step up
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
        best_header = current_header
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
    def dead_constraint(self, log):
        current_header = self.master_node.right
        while current_header != self.master_node:
            # We do not care is non-primary constraints are dead
            if current_header.primary and current_header.size <= 0:
                if log:
                    self.file_write_log_row(current_header, backtrack=True)  # Log this backtrack
                return True
            current_header = current_header.right
        return False

    # Main DLX function: This is where we lose ourselves to dance(Daft Punk).
    # This calls many of the methods above.
    # This is a recursive function, see report for more details
    # Arguments: k = depth of the algorithm
    # Return: None
    def dlx(self, k, log=True):
        #print("Starting algorithm DLX. k=", k)  # DEBUG
        # self.print()  # DEBUG
        # self.print_solution()  # DEBUG
        # If the only constraints remaining are non-primary ones, we have found a solution!
        if not self.master_node.right.primary:
            #print("O frabjous day! Callooh! Callay!")  # DEBUG
            #self.print_solution()  # DEBUG
            # Write this solution to both output files
            self.file_write_solution(True)
            if log:
                self.file_write_solution(False)
            return None
        else:
            # Check to see if there are any dead constraints
            if self.dead_constraint(log):
                #print("Dead constraint, need to backtrack")  # DEBUG
                # Return as the problem is not well defined anymore
                return None
            # Choose the column with the smallest size, by calling the find_best_constraint function
            current_column = self.find_best_column()
            # Best column now found
            #print("Best column found, ", current_column.name)  # DEBUG
            # Branch now for each row in this column
            current_node = current_column.down  # Start below the column header, iterate down from here
            self.cover_column(current_column)  # First cover this column
            while current_node != current_column:
                self.set_solution_k(current_node, k)  # Add this to the solution list, will be overwritten if not a
                # solution.
                # Record this step of the algorithm in the log
                if log:
                    self.file_write_log_row(current_node, k, backtrack=False)
                # Iterate across this row
                current_right = current_node.right
                while current_right != current_node:
                    # Cover the column this node belongs to
                    self.cover_column(current_right.column)
                    current_right = current_right.right  # step right
                # print("Recursive call")  # DEBUG
                # Call dlx again, with depth += 1
                self.dlx(k+1, log)
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


def begin_dlx_n_queen(n, log):
    start_time = time.time()
    print("Solving N Queens problem, for N = ", n)
    print("Creating 1-0 Matrix...")
    one_zero_matrix = create_one_zero_matrix(n)
    populate_one_zero_matrix(one_zero_matrix, n)
    print("Done.")
    print("Solving now for:\n", one_zero_matrix)
    overall_list = FourWayLinkedList("{0}_queen_output.txt".format(n),"{0}_queen_log.txt".format(n))
    overall_list.convert_exact_cover(one_zero_matrix, log)
    overall_list.transform_n_queen(n)
    master_node = overall_list.master_node
    #test_circular_list(master_node)
    overall_list.dlx(0, log)
    print("Algorithm DLX finished, execution time:")
    if overall_list.total_solutions == 0:
        print("It appears no solutions were found for your matrix, the problem may not be well defined")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Output can now be seen in '{0}_queen_output.txt'".format(n))
    return None


def begin_dlx_user_input_matrix(user_input_matrix, log):
    start_time = time.time()
    print("Now solving your favourite matrix:\n", user_input_matrix)
    overall_list = FourWayLinkedList()
    overall_list.convert_exact_cover(user_input_matrix, log)
    master_node = overall_list.master_node
    #test_circular_list(master_node)
    overall_list.dlx(0, log)
    print("Algorithm DLX finished, execution time:")
    if overall_list.total_solutions == 0:
        print("It appears no solutions were found for your matrix, the problem may not be well defined")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Output can now be seen in 'main_output.txt'")
    return None


def test_circular_list(master_node):
    test_right = master_node.right
    while test_right != master_node:
        test_below = test_right.down
        print(test_right.name)
        while test_below != test_right:
            counter = 0
            row_right = test_below.right
            while row_right != test_below:
                counter = counter + 1
                row_right = row_right.right
            test_below = test_below.down
        test_right = test_right.right
    return None


user_interface()
