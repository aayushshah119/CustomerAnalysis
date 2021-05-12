# flake8: noqa
import csv
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from tabulate import tabulate
from datetime import datetime
from typing import Dict, Any, List, Tuple
import sys


class TasteAnalysis:
    LAST_COHORT_END = "2020-07-25 00:00 UTC"  # Saturday
    FIRST_COHORT_START = "2020-04-18 00:00 UTC"
    BEST_CUSTOMER_MIN = 2  # Min is 2 orders

    weeks = [datetime.strptime("2020-04-18", '%Y-%m-%d').date(), datetime.strptime("2020-04-25", '%Y-%m-%d').date(),
             datetime.strptime("2020-05-02", '%Y-%m-%d').date(), datetime.strptime("2020-05-09", '%Y-%m-%d').date(),
             datetime.strptime("2020-05-16", '%Y-%m-%d').date(), datetime.strptime("2020-05-23", '%Y-%m-%d').date(),
             datetime.strptime("2020-05-30", '%Y-%m-%d').date(), datetime.strptime("2020-06-06", '%Y-%m-%d').date(),
             datetime.strptime("2020-06-13", '%Y-%m-%d').date(), datetime.strptime("2020-06-20", '%Y-%m-%d').date(),
             datetime.strptime("2020-06-27", '%Y-%m-%d').date(), datetime.strptime("2020-07-04", '%Y-%m-%d').date(),
             datetime.strptime("2020-07-11", '%Y-%m-%d').date(), datetime.strptime("2020-07-18", '%Y-%m-%d').date(),
             ]

    weeks_dict = dict.fromkeys(weeks)
    for i in range(len(weeks)):
        weeks_dict[weeks[i]] = set()

    """
    Reads in the CSV file and sets member variables as needed
    """

    def __init__(self, path):
        print(f"Processing csv at: {path}")
        self.row_count = 0
        self.customers = {}
        self.frequency_count = {}
        self.dates = {}

        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.row_count += 1
                if row['Email'] in self.customers:
                    self.customers[row['Email']] += 1
                else:
                    self.customers[row['Email']] = 1

                date_obj = datetime.strptime(row['Created (UTC)'], '%m/%d/%y %H:%M').date()
                for i in range(len(self.weeks)):
                    if i + 1 != len(self.weeks):
                        if self.weeks[i] <= date_obj < self.weeks[i + 1]:
                            self.weeks_dict[self.weeks[i]].add(row['Email'])
                            break
                    else:
                        if self.weeks[i] <= date_obj:
                            self.weeks_dict[self.weeks[i]].add(row['Email'])

        for customer in self.customers:
            if self.customers[customer] in self.frequency_count:
                self.frequency_count[self.customers[customer]] += 1
            else:
                self.frequency_count[self.customers[customer]] = 1

        """
       
        YOUR CODE HERE
        Process CSV and store in appropriate data structures
        
        Hint: create a class member data structure to store self.customers, 
              optionally create a data structure to store frequency count
       
        """

        print("Finished processing: ", self.row_count)
        print("\n\n")

    def gen_reports(self) -> None:
        self.print_best_customers()
        self.print_customer_repeat_rate()
        self.print_weekly_cohort_analysis()

    """
    Prints the best customers. One per line. A 'Best Customer' is
    where the purchase count is greater than or equal to 
    TasteAnalysis.BEST_CUSTOMER_MIN.

    Returns a List of Tuples. Each tuple is a the number of purchases
    made by Best Customer and the customer email.
    """

    def print_best_customers(self) -> List[Tuple[int, str]]:
        print("=====BEST CUSTOMERS=====")
        best_customers: List[Tuple[int, str]] = []
        for customer in self.customers:
            if self.customers[customer] >= self.BEST_CUSTOMER_MIN:
                print(customer)
                best_customers += [(self.customers[customer], customer)]

        print("\n\n")

        return best_customers

    """
    Prints the customer repeat rate
    Total Purchases Count       [Count]
    Unique Customers            [Count]
    1 Count                     [Count]
    ... (continues with 2,3,4,5... if they exist)

    Returns the argument to tabulate: type List[List[Any]]
    """

    def print_customer_repeat_rate(self) -> List[List[Any]]:
        print("=====CUSTOMER REPEAT RATE=====")
        table: List[List[Any]] = []
        table += [["Total Purchases Count", self.row_count]]
        table += [["Unique Customers", len(self.customers)]]

        for i in range(1, self.row_count):
            if i in self.frequency_count:
                table += [[str(i) + " Count", self.frequency_count[i]]]

        print(tabulate(table))
        print("\n\n")
        return table

    """
    Each row has a Cohort Start Date, which are weekly dates starting from 4/18
    
    Total Cohort Customers: are all the unique customers who purchased during that week
    
    Repeat Customers (%): is the number of customers in that week who have purchased 
    in previous weeks. 
    Percent is shown in parenthesis - 100 * Repeat Customers / Total Cohort Customers.

    New Customers (%): is the number of customers who are new that week. 
    Percent is shown in parenthesis - New Customers / Total Cohort Customers.

    Buy Avg: Total Orders made by new customers / New Customers. 
    Where Total Orders extends the entire duration of the data. 
    For example, if 5 customers bought once per week for 8 weeks, 
    then Total Orders is 40 and the Buy Avg = 40/5 = 8.

    Returns the table that tabulate prints
    """

    def print_weekly_cohort_analysis(self) -> List[List[Any]]:
        # calculate repeat purchases by cohort
        print("=====WEEKLY COHORT ANALYSIS=====")

        table = [[
            "Cohort Start Date",
            "Total Cohort Customers",
            "Repeat Customers (%)",
            "New Customers (%)",
            "Buy Avg",
        ]]

        for i in range(len(self.weeks)):
            total_customers = len(self.weeks_dict[self.weeks[i]])
            repeat_customers = 0
            new_customers = set.copy(self.weeks_dict[self.weeks[i]])

            for customer in self.weeks_dict[self.weeks[i]]:
                for j in range(i):
                    if customer in self.weeks_dict[self.weeks[j]]:
                        repeat_customers += 1
                        new_customers.remove(customer)

            total_orders = 0
            for customer in new_customers:
                total_orders += self.customers[customer]

            if len(new_customers) == 0:
                buy_avg = "-"
            else:
                buy_avg = round(total_orders / len(new_customers), 2)

            if total_customers != 0:
                repeat_customers_per = 100 * repeat_customers // total_customers
                repeat_customers_str = f"{repeat_customers} ({repeat_customers_per}%)"

                new_customers_per = 100 * len(new_customers) // total_customers
                new_customers_str = f"{len(new_customers)} ({new_customers_per}%)"
            else:
                repeat_customers_str = "0"
                new_customers_str = "0"

            table.append([str(self.weeks[i]), str(total_customers), repeat_customers_str, new_customers_str, buy_avg])

        print(tabulate(table, headers="firstrow"))
        return table


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter a valid csv file path")
    else:
        csv_path = sys.argv[1]
        assert csv_path is not None

        analyzer = TasteAnalysis(csv_path)
        analyzer.gen_reports()
