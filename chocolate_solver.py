from collections import defaultdict
import math
import random
import copy

class ChocolateSolver():

    distributions = []
    cuts_made = 0
    verbose = True

    def processLengths(self, bar_lengths, desired_lengths, is_verbose):
        """Calculates minimum number of cuts to distribute desired lengths from given bar lengths

        Parameters
        ----------
        bar_lengths: list of ints
        desired_lengths: List of ints
        is_verbose: boolean

        Returns
        -------
        int: The calculated minimum number of cuts
        """

        self.verbose = is_verbose

        # Step 1:
        # If there is not enough chocolate to meet desired amount then no solution is available
        if sum(bar_lengths) < sum(desired_lengths):
            print("No solution available: not enough chocolate to satisfy requested amounts, all children will go hungry.")
            return -1


        if self.verbose:
            print()
            print(f"Checking for perfect matches")
            print()

        # Step 2:
        # Remove any perfect matches
        # Start by adding lengths to a dictionary of lengths arrays - O(m)
        bar_length_dict = defaultdict(int)
        for length in bar_lengths:
            bar_length_dict[length] += 1
        # Then filter out desired lengths by checking membership in the bar length dictionary - O(n)
        new_desired_lengths = []
        for length in desired_lengths:
            if bar_length_dict[length] >= 1:
                bar_length_dict[length] -= 1
                self.addAction(f"Distribute {length} to child that wants {length}")
            else:
                new_desired_lengths.append(length)

        # Rebuild the lists
        desired_lengths = new_desired_lengths
        bar_lengths = []
        for item in bar_length_dict.keys():
            for amount in range(bar_length_dict[item]):
                bar_lengths.append(item)

        if self.verbose:
            print()
            print(f"Checking for additive combinations")
            print()

        # Step 3:
        # Test for additive combinations - O(n*m*k)
        desired_lengths, bar_lengths = self.checkAdditiveCombinations(desired_lengths, bar_lengths)

        if self.verbose:
            print()
            print(f"Beginning naive Monte Carlo heuristic")
            print()


        # Work in progress: Very naive Monte Carlo heuristic
        num_sample_iterations = 20
        self.cuts_made, optimal_actions = self.randomSampling(num_sample_iterations, bar_lengths, desired_lengths)


        return self.cuts_made



    def addAction(self, description):
        # Prints a string to the console if running in verbose mode
        if self.verbose:
            print(description)


    def checkAdditiveCombinations(self, desired_lengths, available_lengths):
        """ Searches for a given length among possible subsets of a list

            Parameters
            ----------
            available_lengths: list of ints
            desired_lengths: List of ints

            Returns
            -------
            list of new desired_lengths
            list of new available_lengths
        """
        for length in desired_lengths:
            combination_available = self.findSubSetSumDP(available_lengths, length)
            if combination_available == False:
                continue
            else:
                self.addAction(f"Distribute {combination_available} to child that wants {length}")
                desired_lengths.remove(length)
                for component_length in combination_available:
                    available_lengths.remove(component_length)

        return desired_lengths, available_lengths

    def findSubSetSumDP(self, candidate_lengths, desired_length):
        """ Searches for a given length among possible subsets of a list

            Time Complexity - O(desired_length * m) -> pseudopolynomial
            Space Complexity - O(desired_length * m)

            Parameters
            ----------
            candidate_lengths: list of ints
            desired_length: int

            Returns
            -------
            list of pieces for the sum, or false if not realizable
        """

        n = len(candidate_lengths)

        # Table of realizable sums
        sum = ([[False for i in range(desired_length + 1)] for i in range(n + 1)])
        # Table of parent pointers
        parent = ([[None for i in range(desired_length + 1)] for i in range(n + 1)])


        # Build the table
        sum[0][0] = True
        for i in range(1, n + 1):
            for j in range(0, desired_length + 1):
                sum[i][j] = sum[i-1][j]
                parent[i][j] = None
                if (j >= candidate_lengths[i-1]) and (sum[i-1][j-candidate_lengths[i-1]] == True):
                    sum[i][j] = True
                    parent[i][j] = j-candidate_lengths[i-1]

        # Check table
        if sum[n][desired_length] != True:
            return False


        pieceList = []

        def reportSubSet(n, k):
            # Recursively follow the parent table to build the solution subset
            if k == 0:
                return
            if parent[n][k] == None:
                reportSubSet(n-1,k)
            else:
                reportSubSet(n-1, parent[n][k])
                pieceList.append(k - parent[n][k])

        # Run the recursive function to retrieve the subset as a list
        reportSubSet(n, desired_length)

        return pieceList


    def randomSampling(self, n_sample_iterations, candidate_lengths, desired_lengths):
        """ Performs random samples of different min_cut solutions

            Parameters
            ----------
            n_sample_iterations: integer number of samples
            candidate_lengths: list of ints
            desired_lengths: list of ints

            Returns
            -------
            int: minimum number of cuts to achieve a solution as found from the random sampling
            list of strings: the actions taken during the best iteration of the random sampling
        """
        lowest_cost = math.inf
        optimal_actions = []

        for i in range(n_sample_iterations):

            candidate_length_copy = copy.deepcopy(candidate_lengths)
            desired_length_copy = copy.deepcopy(desired_lengths)

            # Sample a random solution
            current_cost, actions_taken = self.randomSolution(candidate_length_copy, desired_length_copy)

            if self.verbose:
                print(f"Random solution obtained with cost: {current_cost}")
                print()

            if current_cost < lowest_cost:
                lowest_cost = current_cost
                optimal_actions = actions_taken

        return lowest_cost, optimal_actions

    def randomSolution(self, candidate_lengths, desired_lengths):
        """ Gets a random solution to a min_cut problem instance

            Parameters
            ----------
            candidate_lengths: list of ints
            desired_lengths: list of ints

            Returns
            -------
            int: minimum number of cuts in this solution instance
            list of strings: list of the actions taken for this sample
        """
        sample_cuts = 0
        # Array for storing the actions taken while running
        actions_taken = []

        while len(desired_lengths) > 0:

            # Get a random subset from desired_lengths equal to 1/4 of the remaining elements (+ 1 to account for single element list)
            desired_length_count = len(desired_lengths)
            sample_count = math.floor(desired_length_count/4) + 1
            random_desired_lengths = random.sample(desired_lengths, sample_count)

            # Greedily make cuts to fit a desired length - O(n*m)
            remove_list = []
            for length in random_desired_lengths:
                # Find the element that is largest and cut it to size
                for index,candidate_length in enumerate(candidate_lengths):
                    if candidate_length > length:
                        self.addAction(f"Cut {candidate_length} to {length} for child that wants {length}")
                        sample_cuts += 1
                        remainder_length = candidate_length - length
                        candidate_lengths[index] = remainder_length
                        remove_list.append(length)
                        break

            # Filter the above solved elements from the desired_lengths
            for element in remove_list:
                desired_lengths.remove(element)

            # Test again for additive combinations - O(n*m*k)
            desired_lengths, candidate_lengths = self.checkAdditiveCombinations(desired_lengths, candidate_lengths)


            if len(desired_lengths) == 0:
                break


            # Greedily add small values to create desired lengths - O(n*m)
            candidate_lengths.sort()
            desired_lengths.sort()
            remove_list = []
            early_stop = False
            for desired_length in desired_lengths:
                additive_length = 0
                component_lengths = []
                length_acquired = False
                for index,candidate_length in enumerate(candidate_lengths):
                    # If values are becoming larger then proceed to next heuristic (greedy cutting)
                    if candidate_length > desired_length:
                        early_stop = True
                        break

                    new_length = additive_length + candidate_length
                    if new_length <= desired_length:
                        additive_length += candidate_length
                        component_lengths.append(candidate_length)
                        candidate_lengths.pop(index)
                    else:
                        length_surplus = new_length - desired_length
                        desired_portion = candidate_length - length_surplus
                        candidate_lengths[index] = length_surplus
                        self.addAction(f"Cut {candidate_length} to {length_surplus}")
                        sample_cuts += 1
                        component_lengths.append(desired_portion)
                        additive_length += desired_portion
                    if additive_length == desired_length:
                        self.addAction(f"Distribute {component_lengths} to child that wants {desired_length}")
                        remove_list.append(desired_length)
                        lengthAcquired = True
                        break
                # Proceed to next heuristic
                if early_stop:
                    break

            for element in remove_list:
                desired_lengths.remove(element)

            # Test again for additive combinations - O(n*m*k)
            desired_lengths, candidate_lengths = self.checkAdditiveCombinations(desired_lengths, candidate_lengths)

            if len(desired_lengths) == 0:
                break


        return sample_cuts, actions_taken
