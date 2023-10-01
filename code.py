from itertools import product

class Category:
    def __init__(self, this_category):
        self.this_category = this_category
        self.ledger = []
        self.actions = []
        self.max_chars = 30
        self.final_total = 0
        self.withdrawn = 0

    def record_action(self, action_description):
        self.actions.append(action_description)

    def deposit(self, added_amount, description="None"):
        self.ledger.append({"amount": added_amount, "description": description})
        length_of_number = len(str(added_amount))
        space_left = self.max_chars - len(description) - length_of_number - 4
        my_float = "{:.2f}".format(added_amount / 1.0)
        if len(description) > 24:
            description = description[:19]
            self.record_action(f"{description}...{' ' * space_left}+{my_float}")
        else:
            self.record_action(f"{description}{' ' * space_left}+{my_float}")
        self.final_total += added_amount

    def withdraw(self, amount, description="None"):
        if self.check_funds(amount):
            length_of_number = len(str(amount))
            space_left = self.max_chars - len(description) - length_of_number - 4
            my_float = "{:.2f}".format(amount / 1.0)
            self.withdrawn += amount
            if len(description) > 24:
                description = description[:19]
                self.record_action(f"{description}...{' ' * space_left}-{my_float}")
            else:
                self.record_action(f"{description}{' ' * space_left}-{my_float}")

            self.final_total -= amount
            return True
        else:
            self.record_action(f"Withdrawal of {amount} failed - {description}")
            return False

    def get_balance(self):
        return self.final_total

    def transfer(self, this_amount, category):
        this_amount = int(this_amount)
        if self.check_funds(this_amount):
            self.withdraw(this_amount, f"Transfer to {category.this_category}")
            category.deposit(this_amount, f"Transfer from {self.this_category}")
            return True
        else:
            self.record_action(f"Transfer of {this_amount} to {category.this_category} failed")
            return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        final_list = []
        category_len = len(self.this_category)
        stars = self.max_chars - category_len
        stars //= 2
        title = (('*' * stars) + (self.this_category) + ('*' * stars))
        # Include action log in the output
        action_log = "\n".join(self.actions)
        # Determine the maximum width for the numbers
        max_num_width = max(len(str(entry["amount"])) for entry in self.ledger)
        my_float = "{:.2f}".format(self.final_total / 1.0)
        for entry in self.ledger:
            formatted_entry = ""
            for key, value in entry.items():
                # Exclude 'amount' and 'description' keys
                if key not in ['amount', 'description']:
                    # Append the key-value pair with right alignment and additional padding
                    formatted_entry += f"{key}: {value:>{max_num_width}.2f}" + " " * (len(title) - len(self.this_category) - 1)
            final_list.append(formatted_entry)

        total_formatted = "{:.2f}".format(self.get_balance() / 1.0)
        return "\n"+title + ''.join(final_list) + "\n" + action_log + "\n" + "Total: " + str(my_float)

food = Category("Food")
shopping = Category("Shopping")
it = Category("It")
clothing = Category("Clothing")
food.deposit(500, "initial deposit")
food.withdraw(20, "groceries")
food.deposit(30, "weekly bonus")
food.transfer(300, shopping)
shopping.withdraw(50,"some spendings on pizza")
print(food)
print(shopping)


def create_spend_chart(list_of_categories):
    print("\nPercentage spent by category")
    for percent in range(100, -1, -10):
        print(f" {percent:3} |", end="")

        for category in list_of_categories:
            if category.final_total == 0:
                percentage = 0
            else:
                percentage = (category.withdrawn * 100) // category.final_total

            if percentage >= percent:
                bar = "o"
            else:
                bar = " "

            print(f" {bar} ", end="")
        print()

    print("     -" + "---" * (len(list_of_categories)))

    names = [category.this_category for category in list_of_categories]
    max_len = max(len(name) for name in names)

    for i in range(max_len):
        print("     ", end="")
        for name in names:
            if i < len(name):
                print(f" {name[i]} ", end="")
            else:
                print("   ", end="")
        print()


create_spend_chart([food, shopping, it, clothing])
