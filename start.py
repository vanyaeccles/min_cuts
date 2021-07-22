import sys
from chocolate_solver import ChocolateSolver


def checkInputFormatting(inputString):
    """ Checks that the input string is of the form '{int,int,int}'

        Parameters
        ----------
        inputString: a string

        Returns
        ----------
        A list of the integers contained in the string, or returns an error with an explanation
    """
    try:
        if inputString[0] != '{' or inputString[-1] != '}':
            raise ValueError

        inputString = inputString[1:-1]
        inputAsArray = [int(x) for x in inputString.rstrip().split(',')]
        return inputAsArray

    except ValueError:
        print("Input Error: Please enter in the form: {int1,int2,int3,int7}")
        return -1



def main(is_verbose):
    while(1):

        chocolateSolver = ChocolateSolver()

        # Alternatively inputs can be specified in the script
        # Each of length 100
        desiredLengths = [5, 9, 33, 41, 42, 19, 9, 20, 12, 30, 29, 25, 40, 2, 28, 31, 29, 36, 5, 48, 20, 20, 24, 9, 2, 46, 6, 48, 49, 34, 43, 2, 10, 27, 27, 11, 16, 9, 25, 28, 12, 21, 47, 2, 49, 39, 35, 28, 16, 43, 20, 26, 5, 42, 47, 6, 12, 42, 22, 11, 3, 37, 6, 40, 3, 30, 15, 2, 33, 11, 41, 40, 33, 28, 7, 25, 6, 40, 19, 9, 46, 9, 17, 25, 28, 4, 17, 28, 39, 16, 1, 46, 39, 32, 45, 28, 28, 41, 3, 32]
        barLengths = [90, 90, 51, 55, 57, 86, 78, 60, 58, 51, 81, 86, 94, 5, 13, 78, 50, 84, 97, 96, 87, 59, 54, 68, 80, 72, 50, 85, 85, 84, 17, 23, 2, 44, 6, 39, 15, 81, 27, 3, 34, 33, 92, 80, 40, 84, 56, 27, 88, 56, 39, 80, 21, 13, 88, 52, 36, 81, 64, 1, 60, 24, 63, 25, 58, 14, 47, 85, 76, 81, 79, 33, 71, 75, 48, 93, 31, 36, 41, 4, 6, 72, 74, 87, 84, 1, 75, 64, 49, 20, 98, 64, 46, 58, 14, 26, 52, 38, 83, 35]


        if 'barLengths' not in locals():
            # Request and validate the bar length inputs
            barLengthInputMessage = "Please enter the chocolate bar lengths in the form of {length1,length2,lengthN}:"
            barLengthInput = input(barLengthInputMessage)
            barLengths = checkInputFormatting(barLengthInput)

        if barLengths == -1:
            continue

        if 'desiredLengths' not in locals():
            # Request and validate the desired length inputs
            desiredLengthInputMessage = "Please enter the desired lengths of chocolate in the form of {desiredAmount1,desiredAmount2,desiredAmountN}:"
            desiredLengthInput = input(desiredLengthInputMessage)
            desiredLengths = checkInputFormatting(desiredLengthInput)

        if desiredLengths == -1:
            continue


        print("Processing...")


        result = chocolateSolver.processLengths(barLengths, desiredLengths, is_verbose)


        if result >= 0:
            print(f"Solved with {result} cuts made")
            print()

        input("Press any key to continue")



if __name__ == "__main__":
    is_verbose = False
    # Provide for descriptions of actions taken
    if '-v' in sys.argv:
        is_verbose = True

    main(is_verbose)
