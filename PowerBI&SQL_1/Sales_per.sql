-- Daily Trend for Total Orders
SELECT DAYNAME(order_date) as order_day, COUNT(DISTINCT order_id) AS Total_orders FROM pizza_sales
GROUP BY DAYNAME(order_date);

-- Monthly Trend for Total Orders
SELECT MONTHNAME(order_date) as month_name,  COUNT(DISTINCT order_id) AS Total_orders FROM pizza_sales
GROUP BY MONTHNAME(order_date);

-- Percentage of Sales by Pizza Category
SELECT  pizza_category AS Pizza_category, 
	SUM(quantity) AS Sales_by_category,
    SUM(quantity)/ (SELECT SUM(quantity) FROM pizza_sales) *100 AS Percentage_by_category,
    SUM(total_price) / (SELECT SUM(total_price) FROM pizza_sales) * 100 AS Percentage_Revunue
FROM 
	pizza_sales
GROUP BY 
	pizza_category;
        
-- Percentage of Sales by Pizza Size
SELECT pizza_size AS Pizza_size, 
	SUM(quantity) AS Sales_by_size,
    SUM(quantity)/ (SELECT SUM(quantity) FROM pizza_sales) *100 AS Percentage_by_size,
    SUM(total_price) / (SELECT SUM(total_price) FROM pizza_sales) * 100 AS Percentage_Revunue
FROM 
	pizza_sales
GROUP BY 
	pizza_size;
        
-- Best Sellers
SELECT pizza_name_id AS Pizza_type, 
	SUM(quantity) AS Sales_by_type,
    SUM(total_price) AS Total_revenue
FROM 
	pizza_sales
GROUP BY 
	pizza_name_id
ORDER BY Total_revenue DESC
LIMIT 5;

-- Worst Sellers
SELECT pizza_name_id AS Pizza_type, 
	SUM(quantity) AS Sales_by_type,
    SUM(total_price) AS Total_revenue
FROM 
	pizza_sales
GROUP BY 
	pizza_name_id
ORDER BY Total_revenue