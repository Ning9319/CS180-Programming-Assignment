import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)

def DP_helper(n, H, tile_types, tile_values, i, j, protect, multiplier, memo):
    # Base cases:
    if(H < 0):
        return False
    if(i == n and j == n-1): # reach the right bottom's below
        return True
    if(i == n-1 and j == n): # reach the right bottom's right
        return True
    if(i == n or j == n): # except the above two cases, whenever goes out of the table, return False
        return False
    if(memo[i][j][protect][multiplier] != None):
        return memo[i][j][protect][multiplier]
    

    # Recursive:
    # this part is dealing w/ the tile before moving on
    if(i == 0 or j == 0): 
        tile_type = -1
        tile_value = -1
    else: # stepping on the grid except (0,0)
        tile_type = tile_types[i][j]
        tile_value = tile_values[i][j]
        if(tile_type == 0):
            H -= tile_value
        if(tile_type == 1):
            H += tile_value
        if(tile_type == 2):
            protect = 1
        if(tile_type == 3):
            multiplier = 1

    # Making the options
    opt1 = False
    opt2 = False
    opt3 = False
    opt4 = False
    opt5 = False
    opt6 = False
    # moving right
    opt1 = DP_helper(n, H, tile_types, tile_values, i, j+1, protect, multiplier, memo)
    # moving down
    opt2 = DP_helper(n, H, tile_types, tile_values, i+1, j, protect, multiplier, memo)
    if (tile_type == 0 and protect):
        # use the protect and move right
        opt3 = DP_helper(n, H+tile_value, tile_types, tile_values, i, j+1, 0, multiplier, memo)
        # use the protect and move down
        opt4 = DP_helper(n, H+tile_value, tile_types, tile_values, i+1, j, 0, multiplier, memo)
    if (tile_type == 1 and multiplier):
        # use the multiplier and move right
        opt5 = DP_helper(n, H+tile_value, tile_types, tile_values, i, j+1, protect, 0, memo)
        # use the multiplier and move down
        opt6 = DP_helper(n, H+tile_value, tile_types, tile_values, i+1, j, protect, 0, memo)
    
    memo[i][j][protect][multiplier] = opt1 or opt2 or opt3 or opt4 or opt5 or opt6
    return memo[i][j][protect][multiplier]



def DP(n, H, tile_types, tile_values):
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.
    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.
    memo = [[[[None for _ in range(2)] for _ in range(2)] for _ in range(n)] for _ in range(n)]
    res = DP_helper(n, H, tile_types, tile_values, 0, 0, 0, 0, memo)
    # By defualt we return False
    # TODO you should change this

    return res


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
