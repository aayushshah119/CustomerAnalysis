# CustomerAnalysis

# Data Structures

- The first decision that I took with respect to the data structure was to store the csv file in the form of a dictionary using DictReader. This ensured that even if I have multiple other columns, my code would not break.
- Next, I chose customers to be a dictionary <customer_email, count> to save the number of times a customer makes a purchase. Since the order did not matter and I wanted a constant time search, a dictionary was the best option. This customers dictionary also proved to be useful while calculating the buying average in Task 4. I chose this over a list of tuples (customer, count) since a list's search time could be N in worst case.

- I again used a dictionary <DateTime Object,customer_email> to represent the emails of all those who bought in a given week. This representation was particularly useful when finding the total customers/new customers for Task 4. This was particulalry efficient since given each row with its purchase date, I would add it to the dictionary of the weeks as and when its read. It was a bit inefficient since for each row, I had to go through the entire list to see where the date fits in. However, since the size of the weeks list was fixed to 15 it was not increasing the runtime substantially. 
-Also chose to have a frequency_count for the frequency of the number of times n purchaces were made. I was dependent on the created self.customers to create this dicitonary. 

# Testing Strategy

- First step was to ensure that it passed on tiny_customers. Next step was to write the test cases for partial_customers. -The challenge out here was that the partial_customers table was not a small table to directly see the answer. Hence, I relied on pandas and Jupyter notebook to first figure out the correct answers and then use those to check the correctness of my python code.
- I however noticed that the partial_customers only relied on two weeks of data. Hence, I added fake data in random dates to check that the Task 4 works as expected. 

# Algorithms/Interesting/Difficult Tidbits

- For buying average, I was able to reuse my data strcuture of customers. For buying average, we only cared about the orders made by new customers. However, it would be inefficient to go through all the future weeks to find out the total orders made by one person. I instead chose to use the customers dictionary to get the count of the purchases made by a customer. Since this customer is new for this week, we are ensured that all of his purchases are made in the current week and in future weeks.
- I usually believe in having the main chunk of computation be done in the init method itself. Hence, I had to ensure that all the data structures were ready in the init method such that the later methods could be implemented using the minimum required lines of code. 
- I particularly did not have much expereince with the tabulate, datetime module and the importing csv files in Python. However, online documentation and YouTube videos proved to be effective.
- It also took me sometime to understand the buying average portion. I had trouble understanding why it was 1.09 for the tiny_customers. However, exploring the data and reading the specs again did help resolve the confusion!
- I utilized several date structures to make the task more clean and easier. While it could be solved using less data structures, my approach is more cleaner and easier to debug!
- Earlier, I mistook the new customers part as that we only had to compare the customers for this week with the previous week instead of all the previous weeks. Hence, in my earlier implementation, I simply had saved two weeks worth of data. However, I was able to make it compatitble with what the specs asked by simplying looping through all the data of the weeks preceding the current week.


