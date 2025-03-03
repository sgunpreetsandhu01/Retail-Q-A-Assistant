
few_shots = [
    {
        'Question':"How many t-shirts do we have left for nike extra small size and white color?",
        'SQLQuery':"SELECT stock_quantity FROM t_shirts WHERE brand = 'NIKE' AND color = 'White' AND size = 'XS'",
        'SQLResult':"Result of the SQL query",
        'Answer':'55'
    },
    {
        'Question': "How much is the price of the inventory for all small size t-shirts?",
        'SQLQuery':"SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
        'SQLResult': "Result of the SQL query",
        'Answer': '14502'
     },
    {
        'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?" ,
        'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
                        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
                        group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer': '28911.8'
    },
    {
        'Question': "How many white color Levi's shirt I have?",
        'SQLQuery' : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
        'SQLResult': "Result of the SQL query",
        'Answer' : '148'
    },
    {
        'Question': "how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
        'SQLQuery' : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
                        (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
                        group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id""",
        'SQLResult': "Result of the SQL query",
        'Answer' : "3967"
    }

]