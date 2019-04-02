# Insight_Data_Engineer_CC
Code challenge of insight data engineer program at June 2019 by Xiaoling Zhai.

0. Introduction to the repository and how to run the source code.
Source code is in the src folder: purchase_analytics.py (Python3). Only the Python standard library sys is used to pass the arguments.

When running the source, code, use such a commond in the file Insight_Data_Engineer_CC:
python3 ./src/purchase_analytics.py ./input/order_products.csv ./input/products.csv ./output/report.csv
Input files order_products.csv and products.csv are saved in the folder input in Insight_Data_Engineer_CC.

1. Algorithms and complexity analysis
Our targets are number_of_orders and number_of_first_orders. We first of all created a map product_departments (product_i->{ department_i1, department_i2, ...}) which maps each product_id to the departments which it belongs to. Then we traverse the file products.csv to fill
the map product_departments.

Next we created a map department_requests (department_i-> [number_of_orders, number_of_first_orders ]) to record the product requests of each department. We traversed the file order_products.csv. In each record, we read the
product_id, then look up the corresponding department_id from the map product_departments. We will add 1 to the number_of_orders of this department_id and also add 1 to the number_of_first_orders if reordered==0. We can get
the ratio by dividing number_of_first_orders with number_of_orders.

Assume there are N rows in order_products.csv and M rows in products.csv. Then the complexity of this algorithm is O(N+M). Because the searching and adding time complexity in a map and a set is O(1).

2. Edge Cases 
2.1 How to read a csv file? How to make sure a record is legal?
Both input files are csv files with embedded commas and embeded double-quote characters. 
I wrote a function readLineCSV to split a line from a csv file. This function can handle all four formats of a csv file:
1997,Ford,E350
"1997","Ford","E350"
1997,Ford,E350,"Super, luxurious truck"  (with embedded commas)
1997,Ford,E350,"Super, ""luxurious"" truck" (with embedded double-quote characters)

Then I will check whether the length of the returned list of strings is 4, and whether these fields (department_id, product_id, order_id and so on) are integers. If not, just give up this line. 

2.2. A product appears in more than 1 departments in products.csv.
I think this product belongs to all these departments.
We make product_departments[product_id] point to a set of departments, which can hold more than one departments.

2.3. A product appears in order_products.csv but not in products.csv
When we search the department_id of this product in the map product_deparments, it fails.
We will check whether the product is in the map product_deparments. If it is not in, we don't count this product in any department. Because we can not get its department information from our input files.

2.4 Some lines are copies of other lines in file products.csv
So the record telling the product_id belongs to the department_id will occur more than once in the products.csv, which might cause the product's requests in the same department are counted twice.
Then we make product_departments[product_id] point to a set of departments, which will make sure each department_id in product_departments[product_id] is unique.

2.5 Some lines are copies of other lines in file order_products.csv or illegal.
I think a request of a product should have a unique combination (order_id, add_to_cart_order) because in the same order, each product should be put into the cart in a order. So two records with the same (order_id, add_to_cart_order) are copies or illegal.
So I will use a set to save the (order_id, add_to_cart_order) of each request. If the current request has the same (order_id, add_to_cart_order) as one in the set, I will think the current record is a copy of a 
above record or illegal.


3. Test
3.1 Unit Test
I tested the function readLineCSV in Jupyter notebook for all 4 csv input patterns, all passed.
1997,Ford,E350
"1997","Ford","E350"
1997,Ford,E350,"Super, luxurious truck"  (with embedded commas)
1997,Ford,E350,"Super, ""luxurious"" truck" (with embedded double-quote characters)

I also tested the 3 other class methods in the Jupyter notebook to make sure they are functioning as expected.

3.2 My Own Integration Test
I made 5 my own integration test cases, all passed. Each test is saved in one folder of your-own-test_1, your-own-test_2, your-own-test_3, your-own-test_4, your-own-test_5, which corresponds to edge case. For example, your-own-test_3 corresponds to edge case 2.1, 2.2, 2.3, 2.4, and 2.5.

3.3 Integration Test Using order_products_train.csv from Instacart, all passed.
I made 3 integration test.
test_1: inputs are order_products_train.csv, products.csv
test_1: inputs are examples of order_products.csv, products.csv from https://github.com/InsightDataScience/Purchase-Analytics
test_3: inputs are order_products_prior.csv, products.csv


