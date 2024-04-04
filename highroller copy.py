"""
Name: Nathan Trifunovic
Date: April 2, 2024
Description: roll sets of dice with different commands displaying results and values of dice
"""

from random import randint


class Die():
    """
    ####### Die Class: ######
    A simple class for representing die objects. A die has a given number of
    sides (at least) four, set when the die is constructed and which can never
    be changed. The die's value can be changed, but only by calling its roll()
    method.
    """

    def __init__(self, initial_value, sides):
        """
        Constructs a die with the given starting value and number of sides.
        """
        if sides < 4 or sides > 99:
            raise ValueError("A die must have between 4 and 99 sides.")
        self.value = initial_value
        self.sides = sides

    def roll(self):
        """
        Simulates a roll by randomly updating the value of this die. 
        In addition to mutating the die's value, this method also 
        returns the new updated value.
        """
        self.value = randint(1, self.sides)
        return self.value

    def get_number_sides(self):
        """ 
        Returns the number of sides of this die.
        """
        return self.sides

    def get_current_value(self):
        """
        Returns the current value of this die.
        """
        return self.value

    def __str__(self):
        """
        Returns a string representation of this die, which is its value enclosed in square
        brackets, without spaces, for example "[5]".
        """
        #return "[" + str(self.value) + "]"
        return f"[{self.value}]"


class DiceSet():
    """
    ####### DiceSet Class: ######
    A dice set holds a collection of Die objects. All of the die objects have
    the same number of sides. 
    """

    def __init__(self, sides_each_die, number_of_dice):
        """
        Creates a DiceSet containing the given number of dice, each with the 
        given number of sides. All die values start off as 1.
        """
        if number_of_dice < 2 or number_of_dice > 99:
            raise ValueError("You need to have between 2 to 99 dice")

        self.dice = []
        for i in range(number_of_dice):
            self.dice.append(Die(1, sides_each_die))
        
        self.sides_each_dice = sides_each_die

    def get_descriptor(self):
        """
        Returns the descriptor of the dice set; for example "5d20" for a set with
        five dice of 20 sides each; or "2d6" for a set of two six-sided dice.
        """
        #return str(len(self.dice)) + "d" + str(self.sides_each_dice)
        return f"{len(self.dice)}d{self.sides_each_dice}"

    def get_total(self):
        """
        Returns the total of the values of each die in the set.
        """
        return sum(die.get_current_value() for die in self.dice)

    def roll_all(self):
        """
        Rolls all the dice in the set.
        """
        return [die.roll() for die in self.dice]

    def roll_die(self, i):
        """
        Rolls the i-th die (0-indexed). In addition to mutating the die's value,
        this method also returns the new updated value.
        """
        if 0 <= i < len(self.dice):
            return self.dice[i].roll()

    def get_current_values(self):
        """
        Returns the values of each of the dice in a list.
        """
        return [die.get_current_value() for die in self.dice]

    def matches(self, dice_set):
        """
        Returns whether this dice set has the same distribution of values as
        another dice set. The two dice sets must have the same number of dice
        and the same number of sides per dice, and there must be the same
        number of each value in each set.
        """


    def __str__(self):
        """
        Returns a string representation in which each of the die strings are
        joined without a separator, for example: "[2][5][2][3]".
        """
        string = ""
        for die in self.dice:
            string += str(die)
        return string.strip()


def main():
    """ 
    ####### Main Program: ######
    The program should begin by printing a welcome message. 
    Then it repeatedly asks the user to enter a command and carries
    it out. Each command will either print a response or an error 
    message, followed by a blank line.
    """
    # TODO: Write your main program here, then remove pass
    print("Welcome to the High Roller!")
    dice_set = None
    
    print("\nPlease enter a number for a command:",
              "\n1. Load dice set", "\n2. Total dice values", 
              "\n3. Dice set description", "\n4. Current dice values", 
              "\n5. Roll specific dice","\n6. Highest dice"
              "\nq. Quit", "\n?. Help")

    while True:
        
        cmd = input()
        
        if cmd.lower() == "q" or cmd.lower() == "quit":
            print("Have a nice day!")
            break
        elif cmd == "?" or cmd.lower() == "h" or cmd.lower() == "help":
            print("\nPlease enter a number for a command:",
              "\n1. Load dice set", "\n2. Total dice values", 
              "\n3. Dice set description", "\n4. Current dice values", 
              "\n5. Roll specific dice","\n6. Highest dice"
              "\nq. Quit", "\n?. Help")
            

        else: 
            try:
                answer = int(cmd)
                if answer == 1:
                    try:
                        a = int(input("How many sides: "))
                        #b = int(input("How many dice: "))
                        if a < 4 or a > 99:
                            print("A die must have between 4 and 99 sides.")
                            continue
                        
                        
                        b = int(input("How many dice: "))
                        if b < 2 or b > 99:
                            print("There needs to be a number of dice between 2 and 99.")
                            continue

            
                        dice_set = DiceSet(a,b)
                        dice_set.roll_all()
                    except ValueError:
                        print("Please enter an valid number...")


                #elif answer == 2:
                #    if dice_set is not None:
                #        print("Rolling all dice:", dice_set.roll_all())
                #    else:
                #        print("Please Load the dice set first")
            
            
                elif answer == 2:
                    if dice_set is not None:
                        print("Total of dice values:", dice_set.get_total())
                    else:
                        print("Please Load the dice set first")
            
        
                elif answer == 3:
                    if dice_set is not None:
                        print("Dice set description:", dice_set.get_descriptor())
                    else:
                        print("Please Load the dice set first")


                elif answer == 4:
                    if dice_set is not None:
                        print("Current dice values:", dice_set)
                    else:
                        print("Please Load the dice set first")
                

                elif answer == 5:
                    if dice_set is not None:
                        try:
                            x = int(input(f"Which of the {len(dice_set.dice)} dice would you like to roll (1-{len(dice_set.dice)})? "))
                            x -= 1  # Adjust for 0-indexing
                            if 0 <= x < len(dice_set.dice):
                                # Capture the old value
                                old_value = dice_set.dice[x].get_current_value()
                                # Roll the die
                                new_value = dice_set.dice[x].roll()
                                print(f"Old Value: {old_value}\nNew Value: {new_value}")
                            else:
                                print(f"Please enter a number between 1 and {len(dice_set.dice)}.")
                        except ValueError:
                            print("Invalid input. Please enter a numeric value.")
                    else:
                        print("Please Load the dice set first")


                elif answer == 6:
                    if dice_set is not None:
                        highest = max(dice_set.get_current_values())
                        print(f"The highest values is {highest}")
                    else:
                        print("Please Load the dice set first")


                else:
                    print("Please enter a valid command.")

            
            except ValueError:
                print("Please enter an valid command.")


# Run this file to test your main program!
if __name__ == '__main__':
    main()
