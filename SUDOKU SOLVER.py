"""
Sudoku Solver using Backtracking Algorithm
==========================================
This program solves 9x9 Sudoku puzzles using recursive backtracking.
It validates placements and finds solutions efficiently.
"""


class SudokuSolver:
    """
    A class to solve Sudoku puzzles using backtracking algorithm.
    """
    
    def __init__(self):
        """Initialize the solver with a recursion counter."""
        self.recursion_count = 0
    
    def print_board(self, board):
        """
        Print the Sudoku board in a formatted, readable manner.
        
        Args:
            board (list): 9x9 2D list representing the Sudoku grid
        """
        print("\n" + "=" * 37)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 37)
            
            row_str = ""
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += " | "
                
                # Display 0 as empty space for better readability
                if board[i][j] == 0:
                    row_str += " . "
                else:
                    row_str += f" {board[i][j]} "
            
            print(row_str)
        print("=" * 37 + "\n")
    
    def is_valid(self, board, row, col, num):
        """
        Check if placing a number in a specific position is valid.
        
        Args:
            board (list): 9x9 2D list representing the Sudoku grid
            row (int): Row index (0-8)
            col (int): Column index (0-8)
            num (int): Number to place (1-9)
        
        Returns:
            bool: True if placement is valid, False otherwise
        """
        # Check if num already exists in the row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check if num already exists in the column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check if num already exists in the 3x3 subgrid
        # Find the top-left corner of the 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        
        # If all checks pass, the placement is valid
        return True
    
    def find_empty_cell(self, board):
        """
        Find the next empty cell (containing 0) in the board.
        
        Args:
            board (list): 9x9 2D list representing the Sudoku grid
        
        Returns:
            tuple: (row, col) of empty cell, or None if board is full
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None
    
    def solve(self, board):
        """
        Solve the Sudoku puzzle using backtracking algorithm.
        
        Algorithm:
        1. Find an empty cell
        2. Try numbers 1-9 in that cell
        3. For each number, check if it's valid
        4. If valid, place it and recursively try to solve rest
        5. If solving fails, backtrack (remove number and try next)
        6. If no number works, return False to trigger backtracking
        
        Args:
            board (list): 9x9 2D list representing the Sudoku grid
        
        Returns:
            bool: True if puzzle is solved, False if no solution exists
        """
        # Increment recursion counter for statistics
        self.recursion_count += 1
        
        # Find the next empty cell
        empty_cell = self.find_empty_cell(board)
        
        # If no empty cell exists, puzzle is solved
        if empty_cell is None:
            return True
        
        row, col = empty_cell
        
        # Try numbers 1 through 9
        for num in range(1, 10):
            # Check if this number is valid in this position
            if self.is_valid(board, row, col, num):
                # Place the number (make a choice)
                board[row][col] = num
                
                # Recursively attempt to solve with this number placed
                if self.solve(board):
                    return True
                
                # If recursion failed, backtrack (undo the choice)
                board[row][col] = 0
        
        # If no number works, trigger backtracking
        return False
    
    def solve_sudoku(self, board):
        """
        Main method to solve Sudoku and display results.
        
        Args:
            board (list): 9x9 2D list representing the Sudoku grid
        """
        print("Original Sudoku Puzzle:")
        self.print_board(board)
        
        # Reset recursion counter
        self.recursion_count = 0
        
        print("Solving...")
        
        # Attempt to solve the puzzle
        if self.solve(board):
            print("✓ Solution Found!\n")
            print("Solved Sudoku Puzzle:")
            self.print_board(board)
            print(f"Number of recursive calls: {self.recursion_count}")
        else:
            print("✗ No solution exists for this Sudoku puzzle.")
            print(f"Number of recursive calls attempted: {self.recursion_count}")


def get_user_input():
    """
    Allow user to input a Sudoku grid manually.
    
    Returns:
        list: 9x9 2D list representing the user's Sudoku grid
    """
    print("\n" + "=" * 50)
    print("Enter Sudoku Grid (use 0 for empty cells)")
    print("=" * 50)
    print("Enter 9 numbers per row, separated by spaces.")
    print("Example: 5 3 0 0 7 0 0 0 0")
    print()
    
    board = []
    for i in range(9):
        while True:
            try:
                row_input = input(f"Row {i + 1}: ").strip()
                row = [int(x) for x in row_input.split()]
                
                # Validate row length
                if len(row) != 9:
                    print(f"Error: Please enter exactly 9 numbers. You entered {len(row)}.")
                    continue
                
                # Validate number range
                if not all(0 <= num <= 9 for num in row):
                    print("Error: All numbers must be between 0 and 9.")
                    continue
                
                board.append(row)
                break
            except ValueError:
                print("Error: Invalid input. Please enter numbers only.")
    
    return board


def main():
    """
    Main function to run the Sudoku Solver program.
    """
    print("\n" + "=" * 50)
    print("        SUDOKU SOLVER - Backtracking Algorithm")
    print("=" * 50)
    
    # Example Sudoku puzzles (0 represents empty cells)
    
    # Easy puzzle
    example_puzzle_1 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # Hard puzzle
    example_puzzle_2 = [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0]
    ]
    
    # Unsolvable puzzle (for demonstration)
    unsolvable_puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [5, 0, 0, 0, 8, 0, 0, 7, 9]  # Invalid: two 5's in first column
    ]
    
    # Menu for user choice
    print("\nChoose an option:")
    print("1. Solve Example Puzzle 1 (Easy)")
    print("2. Solve Example Puzzle 2 (Hard)")
    print("3. Solve Unsolvable Puzzle (Demo)")
    print("4. Enter Your Own Puzzle")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    solver = SudokuSolver()
    
    if choice == '1':
        # Create a copy to preserve the original
        board = [row[:] for row in example_puzzle_1]
        solver.solve_sudoku(board)
    elif choice == '2':
        board = [row[:] for row in example_puzzle_2]
        solver.solve_sudoku(board)
    elif choice == '3':
        board = [row[:] for row in unsolvable_puzzle]
        solver.solve_sudoku(board)
    elif choice == '4':
        board = get_user_input()
        solver.solve_sudoku(board)
    else:
        print("Invalid choice. Running Example Puzzle 1 by default.")
        board = [row[:] for row in example_puzzle_1]
        solver.solve_sudoku(board)


if __name__ == "__main__":
    main()
