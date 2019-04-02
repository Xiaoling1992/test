import sys

# Define class DepartmentProductOrders to read the input files and generate the report.
class DepartmentProductOrders:
    def __init__(self):
        
        self.product_departments={}; #Edge case 2: product_1: [department_1, department_2......], in case one product belongs to two departments. 
                                     #Edge case 4: if we have repeated records in products.csv.
        self.department_requests={};      #department_1: [number_of_orders,number_of_first_orders]
    
    
    #Read the file order_products.csv to fill the map products_orders     
    def readOrderProducts( self, path_order_products ):
        file_handler = open(path_order_products, "r", encoding="utf-8")
        header=1;
        checkRepeats= set()  #Edge case 5: this set save each request as a tuple (order_id, add_to_cart_order) in the set to exclude these repeated or incorrect order records.
                             #I think it is legal for a product to appear twice in one order, but they should have different add_to_cart_order
        for row in file_handler:
            if header==1:
                header=0;
                continue;                   
            strings = self.readLineCSV( row.strip("\n") )
            if len(strings) !=4:  #Edge case1: give up this line if it doesn't contain 4 segments.
                print("Reading order_products.csv. This line is given up because it does not contains 4 items: "+ row);
                continue;
            
            try:
                order_id= int(strings[0]); #Make sure all four segments in this line are integers.
                product_id= int(strings[1]); 
                add_to_cart_order= int( strings[2] ) #Make sure all four segments in this line are integers.
                reordered= int(strings[3])  #reordered is 1 means the product has been ordered in the past, 0 not;

            except ValueError:  # Edge case 1: give up if the fields in the line desn't have the corret data types 
                print("Could not convert data to an integer.")
            except:
                print("Unexpected error:", sys.exc_info()[0])
            else:
                if (order_id, add_to_cart_order) in checkRepeats: #Edge case 5: If find a repeated record in order_products.csv, continue;
                    print("Repeated order recording: "+ row)
                    continue;
                    
                checkRepeats.add( (order_id, add_to_cart_order) )
                
                if product_id not in self.product_departments: #Edge case 3: If a product of a order is not listed in the products.csv, don not count this product.
                    continue;
                
                for department_id in self.product_departments[product_id]:
                    if department_id not in self.department_requests:   #$$ Question: how to describe the case: if one product is bought twice in a order? Will it has two lines in the order?
                        self.department_requests[ department_id]=[1,0];  #[number_of_orders,number_of_first_orders]
                    else:
                        self.department_requests[ department_id][0]+= 1;
                        
                    if reordered==0:
                        self.department_requests[ department_id][1]+= 1;
        file_handler.close()
                
    #Read the file products.csv to fill the map departmen_products and product_departments   
    def readProducts(self, path_products):
        file_handler= open(path_products)
        header=1;
        
        for row in file_handler:
            if header==1:
                header=0;
                continue;
            strings = self.readLineCSV( row.strip("\n") )
            if len(strings)!= 4:  # Edge case 1: give up if the length is not 4. 
                print("Rading products.csv. This line is given up because it doesn't contain 4 segments: "+ row)
                continue
            
            try:
                product_id= int(strings[0] )
                department_id= int( strings[-1] )
                aisle_id= int( strings[-2] ) #Check whether the second last segment in this line is a number. 
            except ValueError:  # Edge case 1: give up if the fields in the line desn't have the corret data types 
                print("Could not convert data to an integer");
            except:
                print("Unexpected error:", sys.exc_info()[0] )
            else:                    
                if product_id not in self.product_departments:
                    self.product_departments[ product_id ]= { department_id };
                else:
                    self.product_departments[ product_id ].add( department_id );
        file_handler.close()
        
    #Calculate the percentage and write the department_id,number_of_orders,number_of_first_orders,percentage to report.csv
    def getReport(self, path_report):
        file_handler= open(path_report, "w", encoding="utf-8")
        file_handler.write( "department_id,number_of_orders,number_of_first_orders,percentage\n")
        for department_id in sorted( self.department_requests.keys() ):
            
            number_of_orders,number_of_first_orders= self.department_requests[ department_id ]
            percentage= round(number_of_first_orders/number_of_orders, 2) #round to second decimal            
            file_handler.write( "{0},{1},{2},{3:0.2f}\n".format(department_id,number_of_orders,number_of_first_orders,percentage) )
        file_handler.close();   
    
    #Read the CSV files. All 4 cases pass the unit test: '1997,Ford,E350';  '"1997","Ford","E350"';
    #      '1997,Ford,E350,"Super, luxurious truck"';  '1997,Ford,E350,"Super, ""luxurious"" truck"'    
    def readLineCSV(self, line): 
        results=[]
        cur_val=[]
        custom_quote='"'
        separator=','
        in_quotes = False;
        start_collect_char = False;
        double_quotes_in_column = False;
        if not line:
            return results
        if '"' not in line:
            results= line.split( separator)
            return results        
        
        chars=list(line)    
        for ch in chars:
            #state 1: in the quote
            if (in_quotes):
                start_collect_char = True;
                if (ch == custom_quote):
                    in_quotes = False;
                    double_quotes_in_column = False;
                else:
                    #Fixed : allow "" in custom quote enclosed. double_quotes_in_column is only used when custom_quote!='"'
                    if (ch == '\"'):
                        if (not double_quotes_in_column):
                            cur_val.append(ch);
                            double_quotes_in_column = True;           
                    else:
                        cur_val.append(ch);    
        
            #state 2: not in the quote.
            else:
                if (ch == custom_quote):
                    in_quotes = True;  #ch may be the first char '"' of a field, or the second contiguous '"' in a field.
                    
                    #double quotes in column will hit this: '1997,Ford,E350,"Super, ""luxurious"" truck"'
                    if (start_collect_char):
                        cur_val.append('"');
            
                elif (ch == separator):    
                        results.append("".join(cur_val) );
                        cur_val.clear();
                        start_collect_char = False;    
                elif (ch == '\r'):  #ignore LF characters               
                    continue;
                elif (ch == '\n'): #the end, break!                    
                    break;
                else:
                    cur_val.append(ch);     
        results.append(''.join(cur_val) );
        return(results)
            
    
def main(argv):
    department_product_orders= DepartmentProductOrders()
    department_product_orders.readProducts(argv[1]);        #products.csv
    department_product_orders.readOrderProducts(argv[0]);   #order_products.csv
    department_product_orders.getReport(argv[2] );          #path of ouput file report.csv

if __name__ == '__main__':
    if len(sys.argv) != 4:  #The paths of order_products.csv, products.csv, and output file.
        print("Please only input the 3 arguments: path of order_products.csv, products.csv, and output file ")
        raise Exception #$$May need to clarify the type of exception.
    else:
        main(sys.argv[1:])

