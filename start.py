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

    except:
        print("Input Error: Please enter in the form: {int1,int2,int3,int7}")
        return -1



def main(is_verbose):
    while(1):

        chocolateSolver = ChocolateSolver()

        # Request and validate the bar length inputs
        barLengthInputMessage = "Please enter the chocolate bar lengths in the form of {length1,length2,lengthN}:"
        barLengthInput = input(barLengthInputMessage)
        barLengths = checkInputFormatting(barLengthInput)

        if barLengths == -1:
            continue

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





if __name__ == "__main__":
    is_verbose = False
    # Provide for descriptions of actions taken
    if '-v' in sys.argv:
        is_verbose = True

    main(is_verbose)
