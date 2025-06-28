few_shots_list_of_dict = [
    {'Question' : "How many t-shirts do we have LEFT for Nike in XS size AND white color?",
     'SQLQuery' : "SELECT SUM(stock) FROM tshirt_inventory WHERE brand='NIKE' AND color='WHITE' AND size='XS'",
     "Tags": ["SUM", "ORDER BY"]
     },
    {'Question': "How much is the total price of the inventory for all S size t-shirts?",
     'SQLQuery':"SELECT SUM(price*stock) FROM tshirt_inventory WHERE size='S'"
     },
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate post discounts?" ,
     'SQLQuery' : """SELECT SUM(a.total_amount * ((100-COALESCE(discounts.discount_percent,0))/100)) as total_revenue 
                      FROM(select SUM(price*stock) as total_amount, tshirt_id 
                      FROM tshirt_inventory WHERE brand='LEVI' GROUP BY tshirt_id) a 
                      LEFT join discounts ON a.tshirt_id=discounts.tshirt_id"""
     },
    {'Question' : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?" ,
      'SQLQuery': "SELECT SUM(price * stock) FROM tshirt_inventory WHERE brand='LEVI'"
      },
    {'Question': "How many white color Levi's shirt I have?",
     'SQLQuery' : "SELECT SUM(stock) FROM tshirt_inventory WHERE brand='LEVI' AND color='WHITE'"
     },
    {'Question': "how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
     'SQLQuery' : """SELECT SUM(a.total_amount * ((100-COALESCE(discounts.discount_percent,0))/100)) as total_revenue 
                      FROM (select SUM(price*stock) as total_amount, tshirt_id FROM tshirt_inventory 
                      WHERE brand='NIKE' AND size='L' GROUP BY tshirt_id) a 
                      LEFT join discounts ON a.tshirt_id = discounts.tshirt_id"""
    },
    {'Question': "Which brand has the highest total revenue after applying discounts?",
    'SQLQuery': """SELECT tshirt_inventory.brand, SUM(tshirt_inventory.price * tshirt_inventory.stock * 
                      ((100 - COALESCE(discounts.discount_percent, 0)) / 100)) AS total_revenue 
                      FROM tshirt_inventory 
                      LEFT JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id 
                      GROUP BY tshirt_inventory.brand 
                      ORDER BY total_revenue DESC 
                      LIMIT 1"""
    },
    {
    'Question': "What is the percentage of total stock that is currently ON discount?",
    'SQLQuery': """SELECT (SUM(tshirt_inventory.stock * 
                    CASE WHEN discounts.discount_percent IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / 
                    SUM(tshirt_inventory.stock)) AS discount_percentage 
                    FROM tshirt_inventory 
                    LEFT JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id"""
    },
    {
    'Question': "What is the revenue lost due to discounts for all BRANDs?",
    'SQLQuery': """SELECT SUM(tshirt_inventory.price * tshirt_inventory.stock) AS full_PRICE_revenue, 
                    SUM(tshirt_inventory.price*tshirt_inventory.stock*((100-COALESCE(discounts.discount_percent,0))/100)) 
                    AS discounted_revenue, 
                    SUM(tshirt_inventory.price*tshirt_inventory.stock) - 
                    SUM(tshirt_inventory.price*tshirt_inventory.stock*((100-COALESCE(discounts.discount_percent,0))/100)) 
                    AS revenue_lost
                    FROM tshirt_inventory 
                    LEFT JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id"""
    },
    {
    'Question': "Find the top 3 BRANDs that have the highest number of distinct t-shirt models in stock.",
    'SQLQuery': """SELECT brand, COUNT(DISTINCT size) AS model_count 
                    FROM tshirt_inventory 
                    GROUP BY brand 
                    ORDER BY model_count DESC 
                    LIMIT 3"""
    },
    {
    'Question': "What is the ratio of discounted t-shirts to non-discounted t-shirts?",
    'SQLQuery': """SELECT 
                    SUM(CASE WHEN discounts.discount_percent IS NOT NULL THEN 1 ELSE 0 END) AS discounted_count,
                    SUM(CASE WHEN discounts.discount_percent IS NULL THEN 1 ELSE 0 END) AS non_discounted_count,
                    (SUM(CASE WHEN discounts.discount_percent IS NOT NULL THEN 1 ELSE 0 END) * 1.0 /
                    SUM(CASE WHEN discounts.discount_percent IS NULL THEN 1 ELSE 0 END)) AS ratio
                    FROM tshirt_inventory 
                    LEFT JOIN discounts ON tshirt_inventory.tshirt_id = discounts.tshirt_id"""
    },
    {
    'Question': "Which brand has the highest average discount percentage?",
    'SQLQuery': """SELECT tshirt_inventory.brand, AVG(discounts.discount_percent) AS avg_discount 
                    FROM tshirt_inventory 
                    JOIN discounts ON tshirt_inventory.tshirt_id = discounts.tshirt_id 
                    GROUP BY tshirt_inventory.brand 
                    ORDER BY avg_discount DESC 
                    LIMIT 1"""
    },
    {
    'Question': "How many t-shirts have a stock quantity lower than 30 percent of the average stock quantity across all t-shirts?",
    'SQLQuery': """SELECT COUNT(*) 
                    FROM tshirt_inventory 
                    WHERE stock < (SELECT AVG(stock)*0.3 FROM tshirt_inventory)"""
    },
    {
    'Question': "Which size has the highest total revenue generated after applying discounts?",
    'SQLQuery': """SELECT tshirt_inventory.size, 
                    SUM(tshirt_inventory.price*tshirt_inventory.stock*((100-COALESCE(discounts.discount_percent, 0))/100)) 
                    AS total_revenue 
                    FROM tshirt_inventory 
                    LEFT JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id 
                    GROUP BY tshirt_inventory.size 
                    ORDER BY total_revenue DESC 
                    LIMIT 1"""
    },
    {
    'Question': "Find the top 3 colors with the highest stock quantity across all BRANDs.",
    'SQLQuery': """SELECT color, SUM(stock) AS total_stock 
                    FROM tshirt_inventory 
                    GROUP BY color 
                    ORDER BY total_stock DESC 
                    LIMIT 3"""
    },
    {
    'Question': "Which t-shirt brand has the highest discount applied, AND what is the discount percentage?",
    'SQLQuery': """SELECT tshirt_inventory.brand, MAX(discounts.discount_percent) AS max_discount 
                    FROM tshirt_inventory 
                    JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id 
                    GROUP BY tshirt_inventory.brand 
                    ORDER BY max_discount DESC 
                    LIMIT 1"""
    },
    {
    'Question': "Calculate the weighted average price of all t-shirts in stock.",
    'SQLQuery': """SELECT SUM(price*stock)/SUM(stock) AS weighted_avg_PRICE 
                    FROM tshirt_inventory"""

    },
    {
    'Question': "What percentage of the total revenue is generated FROM discounted t-shirts?",
    'SQLQuery': """SELECT (SUM(tshirt_inventory.price*tshirt_inventory.stock*((100-COALESCE(discounts.discount_percent,0))/100)) 
                    * 100.0 / SUM(tshirt_inventory.price*tshirt_inventory.stock)) AS discounted_revenue_percent
                    FROM tshirt_inventory 
                    LEFT JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id"""
    },
    {
    'Question': "Which t-shirt size has the lowest average discount percentage?",
    'SQLQuery': """SELECT tshirt_inventory.size, AVG(discounts.discount_percent) AS avg_discount 
                    FROM tshirt_inventory 
                    JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id 
                    GROUP BY tshirt_inventory.size 
                    ORDER BY avg_discount ASC 
                    LIMIT 1"""
    },
    {
    'Question': "Find the revenue generated FROM all Nike AND Adidas t-shirts that are discounted by at least 20%.",
    'SQLQuery': """SELECT SUM(tshirt_inventory.price*tshirt_inventory.stock*((100-discounts.discount_percent)/100)) 
                    AS revenue 
                    FROM tshirt_inventory 
                    JOIN discounts ON tshirt_inventory.tshirt_id=discounts.tshirt_id 
                    WHERE (tshirt_inventory.brand='Nike' OR tshirt_inventory.brand='Adidas') 
                    AND discounts.discount_percent>=20"""
    },
    {
    'Question': "Find the cumulative stock value of t-shirts for each brand AND display the top 5 BRANDs.",
    'SQLQuery': """SELECT brand, SUM(price * stock) AS stock_value 
                    FROM tshirt_inventory 
                    GROUP BY brand 
                    ORDER BY stock_value DESC 
                    LIMIT 5"""
    }
]