few_shots_list_of_dict = [
    {'Question' : "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "null"},
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$ 21675"},
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer': "26697.050000"} ,
     {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
      'SQLResult': "Result of the SQL query",
      'Answer' : "$ 28228"},
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer' : "255"
     },
    {'Question': "how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
     'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id
 """,
     'SQLResult': "Result of the SQL query",
     'Answer' : "$ 3716.100000"
    },
    {'Question': "Which brand has the highest total revenue after applying discounts?",
    'SQLQuery': """SELECT t_shirts.brand, SUM(t_shirts.price * t_shirts.stock_quantity * 
                      ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) AS total_revenue 
                      FROM t_shirts 
                      LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY t_shirts.brand 
                      ORDER BY total_revenue DESC 
                      LIMIT 1""",
    'SQLResult': "Result of the SQL query",
    'Answer': "Levi"
    },
    {
        'Question': "What is the percentage of total stock that is currently on discount?",
        'SQLQuery': """SELECT (SUM(t_shirts.stock_quantity * 
                      CASE WHEN discounts.pct_discount IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / 
                      SUM(t_shirts.stock_quantity)) AS discount_percentage 
                      FROM t_shirts 
                      LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "14.93762%"
    },
    {
        'Question': "What is the revenue lost due to discounts for all brands?",
        'SQLQuery': """SELECT SUM(t_shirts.price * t_shirts.stock_quantity) AS full_price_revenue, 
                      SUM(t_shirts.price * t_shirts.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      AS discounted_revenue, 
                      SUM(t_shirts.price * t_shirts.stock_quantity) - 
                      SUM(t_shirts.price * t_shirts.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      AS revenue_lost
                      FROM t_shirts 
                      LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "$ 3147.100000"
    },
    {
        'Question': "Find the top 3 brands that have the highest number of distinct t-shirt models in stock.",
        'SQLQuery': """SELECT brand, COUNT(DISTINCT size) AS model_count 
                      FROM t_shirts 
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
                      FROM t_shirts 
                      LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Ratio: 0.21739 (Discounted: 10, Non-discounted: 46)"
    },
    {
        'Question': "Which brand has the highest average discount percentage?",
        'SQLQuery': """SELECT t_shirts.brand, AVG(discounts.pct_discount) AS avg_discount 
                      FROM t_shirts 
                      JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY t_shirts.brand 
                      ORDER BY avg_discount DESC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "Levi - 26.250000% average discount"
    },
    {
        'Question': "How many t-shirts have a stock quantity lower than 30% of the average stock quantity across all t-shirts?",
        'SQLQuery': """SELECT COUNT(*) 
                      FROM t_shirts 
                      WHERE stock_quantity < (SELECT AVG(stock_quantity) * 0.3 FROM t_shirts)""",
        'SQLResult': "Result of the SQL query",
        'Answer': "8 t-shirts"
    },
    {
        'Question': "Which size has the highest total revenue generated after applying discounts?",
        'SQLQuery': """SELECT t_shirts.size, 
                      SUM(t_shirts.price * t_shirts.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      AS total_revenue 
                      FROM t_shirts 
                      LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY t_shirts.size 
                      ORDER BY total_revenue DESC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "S (Small) - 21105.100000"
    },
    {
        'Question': "Find the top 3 colors with the highest stock quantity across all brands.",
        'SQLQuery': """SELECT color, SUM(stock_quantity) AS total_stock 
                      FROM t_shirts 
                      GROUP BY color 
                      ORDER BY total_stock DESC 
                      LIMIT 3""",
        'SQLResult': "Result of the SQL query",
        'Answer': "1. White - 885 units, 2. Blue - 777 units, 3. Black - 740 units"
    },
    {
        'Question': "Which t-shirt model has the highest discount applied, and what is the discount percentage?",
        'SQLQuery': """SELECT t_shirts.model, MAX(discounts.pct_discount) AS max_discount 
                      FROM t_shirts 
                      JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY t_shirts.model 
                      ORDER BY max_discount DESC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "size S - 45% discount"
    },
    {
        'Question': "Calculate the weighted average price of all t-shirts in stock.",
        'SQLQuery': """SELECT SUM(price * stock_quantity) / SUM(stock_quantity) AS weighted_avg_price 
                      FROM t_shirts""",
        'SQLResult': "Result of the SQL query",
        'Answer': "$ 29.3533"
    },
    {
        'Question': "What percentage of the total revenue is generated from discounted t-shirts?",
        'SQLQuery': """SELECT 
                      (SUM(t_shirts.price * t_shirts.stock_quantity * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) 
                      * 100.0 / SUM(t_shirts.price * t_shirts.stock_quantity)) AS discounted_revenue_percentage 
                      FROM t_shirts 
                      LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': "96.48014763449%"
    },
    {
        'Question': "Which t-shirt size has the lowest average discount percentage?",
        'SQLQuery': """SELECT t_shirts.size, AVG(discounts.pct_discount) AS avg_discount 
                      FROM t_shirts 
                      JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                      GROUP BY t_shirts.size 
                      ORDER BY avg_discount ASC 
                      LIMIT 1""",
        'SQLResult': "Result of the SQL query",
        'Answer': "L - 20% average discount"
    },
    {
        'Question': "Find the revenue generated from all Nike and Adidas t-shirts that are discounted by at least 20%.",
        'SQLQuery': """SELECT SUM(t_shirts.price * t_shirts.stock_quantity * ((100 - discounts.pct_discount) / 100)) 
                      AS revenue 
                      FROM t_shirts 
                      JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                      WHERE (t_shirts.brand = 'Nike' OR t_shirts.brand = 'Adidas') 
                      AND discounts.pct_discount >= 20""",
        'SQLResult': "Result of the SQL query",
        'Answer': "$ 2903.200000"
    },
    {
        'Question': "Find the cumulative stock value of t-shirts for each brand and display the top 5 brands.",
        'SQLQuery': """SELECT brand, SUM(price * stock_quantity) AS stock_value 
                      FROM t_shirts 
                      GROUP BY brand 
                      ORDER BY stock_value DESC 
                      LIMIT 5""",
        'SQLResult': "Result of the SQL query",
        'Answer': "1. Levi - $28228, 2. Nike - $22,855, 3. Van Huesen - $19708, 4. Adidas - $18619."
    }
]