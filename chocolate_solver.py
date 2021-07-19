from collections import defaultdict

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

        desired_lengths = new_desired_lengths
        bar_lengths = []
        for item in bar_length_dict.keys():
            for amount in range(bar_length_dict[item]):
                bar_lengths.append(item)

        # Step 3:
        # Test for additive combinations - O(n*m*k)
        desired_lengths, bar_lengths = self.checkAdditiveCombinations(desired_lengths, bar_lengths)

        # Step 4:
        # Greedily add small values to create desired lengths - O(n*m)
        bar_lengths.sort()
        desired_lengths.sort()
        new_desired_lengths = []
        early_stop = False
        for desired_length in desired_lengths:
            additive_length = 0
            component_lengths = []
            length_acquired = False
            for index,candidate_length in enumerate(bar_lengths):
                # If values are becoming larger then proceed to next heuristic (greedy cutting)
                if candidate_length > desired_length:
                    early_stop = True
                    break

                new_length = additive_length + candidate_length
                if new_length <= desired_length:
                    additive_length += candidate_length
                    component_lengths.append(candidate_length)
                    bar_lengths.pop(index)
                else:
                    length_surplus = new_length - desired_length
                    desired_portion = candidate_length - length_surplus
                    bar_lengths[index] = length_surplus
                    self.addAction(f"Cut {candidate_length} to {length_surplus}")
                    component_lengths.append(desired_portion)
                    additive_length += desired_portion
                if additive_length == desired_length:
                    self.addAction(f"Distribute {component_lengths} to child that wants {desired_length}")
                    remove_list.append(desired_length)
                    lengthAcquired = True
                    break
            # Add any rejects for further processing
            if length_acquired == False:
                new_desired_lengths.append(desired_length)
            # Proceed to next heuristic
            if early_stop:
                break

        # Test again for additive combinations - O(n*m*k)
        desired_lengths, bar_lengths = self.checkAdditiveCombinations(desired_lengths, bar_lengths)

        if len(desired_lengths) == 0:
            self.addAction("Returned after step 4")
            return self.cuts_made

        # Step 5:
        # Greedily make cuts - O(n*m)
        # Find first that is larger and cut to size
        remove_list = []
        for length in desired_lengths:
            for index,candidate_length in enumerate(bar_lengths):
                if candidate_length > length:
                    self.addAction(f"Cut {candidate_length} to {length} for child that wants {length}")
                    self.cuts_made += 1
                    remainder_length = candidate_length - length
                    bar_lengths[index] = remainder_length
                    remove_list.append(length)
                    break

        for element in remove_list:
            desired_lengths.remove(element)

        # Test again for additive combinations - O(n*m*k)
        desired_lengths, bar_lengths = self.checkAdditiveCombinations(desired_lengths, bar_lengths)


        if len(desired_lengths) == 0:
            self.addAction("Returned after step 5")
            return self.cuts_made



        # Step 5:
        # Cut any remaining pieces larger than 1 into pieces no larger than 2
        new_bar_lengths = []
        amount_needed = len(desired_lengths)
        small_piece_sum = 0
        for length in bar_lengths:
            even_flag = False
            while length > 2:
                # Alternate between 1,2
                even_flag = not even_flag
                if even_flag:
                    cut_amount = 1
                else:
                    cut_amount = 2
                remainder = length - cut_amount
                self.addAction(f"Cut {length} by {cut_amount} into {remainder}")
                length -= cut_amount
                self.cuts_made +=1
                new_bar_lengths.append(cut_amount)
                small_piece_sum += cut_amount
            # No more cuts needed
            if small_piece_sum >= amount_needed:
                break

        # Test again for additive combinations - O(n*m*k)
        desired_lengths, bar_lengths = self.checkAdditiveCombinations(desired_lengths, new_bar_lengths)

        if len(desired_lengths) == 0:
            self.addAction("Returned after step 5")
            return self.cuts_made


        return self.cuts_made + 1


    def addAction(self, description):
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

            Time Complexity - O(desired_length * m)
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
        #for i in range(n + 1):
        #    sum[i][0] = True
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
            # Build a trace for the distribution list
            if k == 0:
                return
            if parent[n][k] == None:
                reportSubSet(n-1,k)
            else:
                reportSubSet(n-1, parent[n][k])
                pieceList.append(k - parent[n][k])

        reportSubSet(n, desired_length)

        return pieceList
