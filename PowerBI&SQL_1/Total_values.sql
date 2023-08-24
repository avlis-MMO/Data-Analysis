-- Total Revenue
SELECT SUM(total_price) AS Total_Revenue FROM pizza_sales;

-- Average Order Value
SELECT SUM(total_price)/COUNT(DISTINCT order_id) AS Average_order_value FROM pizza_sales;

-- Total Pizzas Sold
SELECT SUM(quantity) AS Total_pizzas_sold FROM pizza_sales;

-- Total Orders
SELECT MAX(order_id) AS Total_orders FROM pizza_sales;

-- Average Pizzas per Order
SELECT CAST(SUM(quantity)/MAX(order_id) AS DECIMAL(10,2)) AS Avg_pizza_oder FROM pizza_sales;