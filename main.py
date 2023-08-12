import random

# Function to generate random test cases and save them in an input file
def generate_test_cases(filename, num_test_cases):
    with open(filename, 'w') as file:
        for _ in range(num_test_cases):
            q = random.randint(1, 10)  # Generate a random number of queries (q) between 1 and 10
            file.write(str(q) + "\n")
            for _ in range(q):
                n = random.randint(1, 100)  # Generate a random number of elements (n) between 1 and 100
                arr = [random.randint(1, 1000) for _ in range(n)]  # Generate n random integers between 1 and 1000
                file.write(" ".join(map(str, arr)) + "\n")

# Function to run the code and save the output in an output file
def save_output(filename_input, filename_output):
    with open(filename_input, 'r') as input_file, open(filename_output, 'w') as output_file:
        for _ in range(int(input_file.readline())):
            q = int(input_file.readline())
            a = []
            cnt = 0
            for x in map(int, input_file.readline().split()):
                nw_cnt = cnt + (len(a) > 0 and a[-1] > x)
                if nw_cnt == 0 or (nw_cnt == 1 and x <= a[0]):
                    a.append(x)
                    cnt = nw_cnt
                    output_file.write('1')
                else:
                    output_file.write('0')
            output_file.write("\n")

if __name__ == "__main__":
    num_test_cases = 5
    input_filename = "input.txt"
    output_filename = "output.txt"

    # Step 1: Generate random test cases and save them in the input file
    generate_test_cases(input_filename, num_test_cases)

    # Step 2: Run the code and save the output in the output file
    save_output(input_filename, output_filename)

