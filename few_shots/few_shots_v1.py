few_shots_list_of_dict = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM tshirt_inventory WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "50"},
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM tshirt_inventory WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$ 18713"},
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from(select sum(price*stock_quantity) as total_amount, t_shirt_id from tshirt_inventory where brand = 'Levi' group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "Result of the SQL query",
     'Answer': "$ 19738.200000 "} ,
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM tshirt_inventory WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : "$ 20312"},
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM tshirt_inventory WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "180"
     },
    {'Question': "how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from (select sum(price*stock_quantity) as total_amount, t_shirt_id from tshirt_inventory where brand = 'Nike' and size="L" group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "Result of the SQL query",
     'Answer' : "$ 5967.500000"
    },
    {'Question': "Which brand has the highest total revenue after applying discounts?",
    'SQLQuery': """SELECT tshirt_inventory.brand, SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity * 
                      ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) AS total_revenue 
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY tshirt_inventory.brand 
                      ORDER BY total_revenue DESC 
                      LIMIT 1""",
    'SQLResult': "Result of the SQL query",
    'Answer': "Adidas, Revenue: 26710.000000"
    },
    {
        'Question': "What is the percentage of total stock that is currently on discount?",
        'SQLQuery': """SELECT (SUM(tshirt_inventory.stock_quantity * 
                      CASE WHEN discounts.pct_discount IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / 
                      SUM(tshirt_inventory.stock_quantity)) AS discount_percentage 
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': " 19.29943 %"
    },
    {
        'Question': "What is the revenue lost due to discounts for all brands?",
        'SQLQuery': """SELECT SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity) AS full_price_revenue, 
                      SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      AS discounted_revenue, 
                      SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity) - 
                      SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      AS revenue_lost
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "$ 4227.500000"
    },
    {
        'Question': "Find the top 3 brands that have the highest number of distinct t-shirt models in stock.",
        'SQLQuery': """SELECT brand, COUNT(DISTINCT size) AS model_count 
                      FROM tshirt_inventory 
                      GROUP BY brand 
                      ORDER BY model_count DESC 
                      LIMIT 3""",
        'SQLResult': "Result of the SQL query",
        'Answer': "1.Van Huesen 5 sizes, 2.Levi	5 sizes, 3.Nike	5 sizes"
    },
    {
        'Question': "What is the ratio of discounted t-shirts to non-discounted t-shirts?",
        'SQLQuery': """SELECT 
                      SUM(CASE WHEN discounts.pct_discount IS NOT NULL THEN 1 ELSE 0 END) AS discounted_count,
                      SUM(CASE WHEN discounts.pct_discount IS NULL THEN 1 ELSE 0 END) AS non_discounted_count,
                      (SUM(CASE WHEN discounts.pct_discount IS NOT NULL THEN 1 ELSE 0 END) * 1.0 /
                      SUM(CASE WHEN discounts.pct_discount IS NULL THEN 1 ELSE 0 END)) AS ratio
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Ratio: 0.21739 (Discounted: 10, Non-discounted: 46)"
    },
    {
        'Question': "Which brand has the highest average discount percentage?",
        'SQLQuery': """SELECT tshirt_inventory.brand, AVG(discounts.pct_discount) AS avg_discount 
                      FROM tshirt_inventory 
                      JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY tshirt_inventory.brand 
                      ORDER BY avg_discount DESC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Levi - 38.333333% average discount"
    },
    {
        'Question': "How many t-shirts have a stock quantity lower than 30% of the average stock quantity across all t-shirts?",
        'SQLQuery': """SELECT COUNT(*) 
                      FROM tshirt_inventory 
                      WHERE stock_quantity < (SELECT AVG(stock_quantity) * 0.3 FROM tshirt_inventory)""",
        'SQLResult': "Result of the SQL query",
        'Answer': "4 t-shirts"
    },
    {
        'Question': "Which size has the highest total revenue generated after applying discounts?",
        'SQLQuery': """SELECT tshirt_inventory.size, 
                      SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      AS total_revenue 
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY tshirt_inventory.size 
                      ORDER BY total_revenue DESC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "L (Large) - 21147.500000"
    },
    {
        'Question': "Find the top 3 colors with the highest stock quantity across all brands.",
        'SQLQuery': """SELECT color, SUM(stock_quantity) AS total_stock 
                      FROM tshirt_inventory 
                      GROUP BY color 
                      ORDER BY total_stock DESC 
                      LIMIT 3""",
        'SQLResult': "Result of the SQL query",
        'Answer': "1. Red - 948 units, 2. Black - 749 units, 3. Blue - 702 units"
    },
    {
        'Question': "Which t-shirt brand has the highest discount applied, and what is the discount percentage?",
        'SQLQuery': """SELECT tshirt_inventory.brand, MAX(discounts.pct_discount) AS max_discount 
                      FROM tshirt_inventory 
                      JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY tshirt_inventory.brand 
                      ORDER BY max_discount DESC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Nike - 45% discount"
    },
    {
        'Question': "Calculate the weighted average price of all t-shirts in stock.",
        'SQLQuery': """SELECT SUM(price * stock_quantity) / SUM(stock_quantity) AS weighted_avg_price 
                      FROM tshirt_inventory""",
        'SQLResult': "Result of the SQL query",
        'Answer': "$ 29.7046"
    },
    {
        'Question': "What percentage of the total revenue is generated from discounted t-shirts?",
        'SQLQuery': """SELECT 
                      (SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      * 100.0 / SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity)) AS discounted_revenue_percentage 
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "95.20653566610%"
    },
    {
        'Question': "Which t-shirt size has the lowest average discount percentage?",
        'SQLQuery': """SELECT tshirt_inventory.size, AVG(discounts.pct_discount) AS avg_discount 
                      FROM tshirt_inventory 
                      JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY tshirt_inventory.size 
                      ORDER BY avg_discount ASC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "S - 16.250000% average discount"
    },
    {
        'Question': "Find the revenue generated from all Nike and Adidas t-shirts that are discounted by at least 20%.",
        'SQLQuery': """SELECT SUM(tshirt_inventory.price * tshirt_inventory.stock_quantity * ((100 - discounts.pct_discount) / 100)) 
                      AS revenue 
                      FROM tshirt_inventory 
                      JOIN discounts ON tshirt_inventory.t_shirt_id = discounts.t_shirt_id 
                      WHERE (tshirt_inventory.brand = 'Nike' OR tshirt_inventory.brand = 'Adidas') 
                      AND discounts.pct_discount >= 20""",
        'SQLResult': "Result of the SQL query",
        'Answer': "$ 4141.500000"
    },
    {
        'Question': "Find the cumulative stock value of t-shirts for each brand and display the top 5 brands.",
        'SQLQuery': """SELECT brand, SUM(price * stock_quantity) AS stock_value 
                      FROM tshirt_inventory 
                      GROUP BY brand 
                      ORDER BY stock_value DESC 
                      LIMIT 5""",
        'SQLResult': "Result of the SQL query",
        'Answer': "1. Adidas - $27232, 2. Nike- $26,370, 3. Levi - $20312, 4. Van Huesen - $14279."
    }
]