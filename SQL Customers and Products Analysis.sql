-- 1. Describe the tables in the database and how they link to each 
-- customers table: contains customer information
-- orders table: contains order information, linked to customers through customerNumber
-- order_details table: contains product information for each order, linked to orders through orderNumber and to products through productCode
-- products table: contains product information classified under a specific product line, linked to productlines through productLine. 

-- 2. Display table data
SELECT 'customers' AS table_name, 
       (SELECT COUNT(*) FROM pragma_table_info('customers')) AS num_attributes, 
       (SELECT COUNT(*) FROM customers) AS num_rows
	  
UNION ALL

SELECT 'products', 
       (SELECT COUNT(*) FROM pragma_table_info('products')), 
       (SELECT COUNT(*) FROM products)

UNION ALL

SELECT 'productlines', 
       (SELECT COUNT(*) FROM pragma_table_info('productlines')), 
       (SELECT COUNT(*) FROM productlines)
	   
UNION ALL

SELECT 'orders', 
       (SELECT COUNT(*) FROM pragma_table_info('orders')), 
       (SELECT COUNT(*) FROM orders)
	   
UNION ALL

SELECT 'orderdetails', 
       (SELECT COUNT(*) FROM pragma_table_info('orderdetails')), 
       (SELECT COUNT(*) FROM orderdetails) 
	   
UNION ALL

SELECT 'payments', 
       (SELECT COUNT(*) FROM pragma_table_info('payments')), 
       (SELECT COUNT(*) FROM payments)
	   
UNION ALL

SELECT 'employees', 
       (SELECT COUNT(*) FROM pragma_table_info('employees')), 
       (SELECT COUNT(*) FROM employees)
	   
UNION ALL

SELECT 'offices', 
       (SELECT COUNT(*) FROM pragma_table_info('offices')), 
       (SELECT COUNT(*) FROM offices)
	   

-- 3. Which Products Should We Order More of or Less of?
WITH Low_Stock AS (
	SELECT p.productCode,
	ROUND(SUM(od.quantityOrdered) * 1.0/p.quantityInStock, 2) AS low_stock
	FROM products p
	JOIN orderdetails od
	ON p.productCode = od.productCode
	GROUP BY 1
	ORDER BY low_stock DESC
	LIMIT 10
),
Product_Performance AS (
	SELECT productCode,
	ROUND(SUM(quantityOrdered * priceEach), 2) AS product_performance
	FROM orderdetails
	WHERE productCode IN (SELECT productCode
                         FROM Low_Stock)
	GROUP BY 1
	ORDER BY product_performance DESC
)
SELECT ls.productCode, ls.low_stock,
		p.productName, p.productLine
FROM Low_Stock ls
JOIN products p
ON ls.productCode = p.productCode
WHERE ls.productCode IN (SELECT productCode FROM Product_Performance)
ORDER BY p.productLine



-- 4. How Should We Match Marketing and Communication Strategies to Customer Behavior?
-- 		(a) how much profit each customer generates.
SELECT o.customerNumber, ROUND(SUM(od.quantityOrdered * (od.priceEach - P.buyPrice)), 2) AS profit
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
JOIN
orders o
ON od.orderNumber = o.orderNumber
GROUP BY 1

--		(b) Finding the VIP and Less Engaged Customers.
-- Top 5 VIP Customers
WITH profit_per_cust AS(
SELECT o.customerNumber, ROUND(SUM(od.quantityOrdered * (od.priceEach - P.buyPrice)), 2) AS profit
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
JOIN
orders o
ON od.orderNumber = o.orderNumber
GROUP BY 1
)
SELECT c.contactLastName, c.contactFirstName, c.city,
		c.country, ppc.profit
FROM customers c
JOIN profit_per_cust ppc
ON c.customerNumber = ppc.customerNumber
ORDER BY ppc.profit DESC 
LIMIT 5

-- Top 5 Least enagaged customers 
WITH profit_per_cust AS(
SELECT o.customerNumber, ROUND(SUM(od.quantityOrdered * (od.priceEach - P.buyPrice)), 2) AS profit
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
JOIN
orders o
ON od.orderNumber = o.orderNumber
GROUP BY 1
)
SELECT c.contactLastName, c.contactFirstName, c.city,
		c.country, ppc.profit
FROM customers c
JOIN profit_per_cust ppc
ON c.customerNumber = ppc.customerNumber
ORDER BY ppc.profit 
LIMIT 5

-- 5. How Much Can We Spend on Acquiring New Customers?
--		(a) Average Profit per customer
WITH profit_per_cust AS(
SELECT o.customerNumber, ROUND(SUM(od.quantityOrdered * (od.priceEach - P.buyPrice)), 2) AS profit
FROM products p
JOIN orderdetails od
ON p.productCode = od.productCode
JOIN
orders o
ON od.orderNumber = o.orderNumber
GROUP BY 1
)
SELECT ROUND(AVG(profit), 2) AS avg_profit
FROM profit_per_cust
