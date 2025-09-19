import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


#1 connect database from mysql

conn = mysql.connector.connect(

         host="localhost",
         user="root",
         passwd="roh4990",
         database="data"

)


if conn.is_connected():
    print("✅ Database connected successfully!")
else:
    print("❌ Connection failed!")



query = """

SELECT C.CUSTOMER_ID , C.NAME , C.LOCATION , SUM(TOTAL_AMOUNT) AS LIFETIME_VALUE FROM SALES_D AS S
JOIN CUSTOMERS_DATA AS C
ON C.CUSTOMER_ID = S.CUSTOMER_ID
GROUP BY CUSTOMER_ID , C.NAME , C.LOCATION 
ORDER BY LIFETIME_VALUE DESC
LIMIT 10;

"""
print(repr(query))

# Query result DataFrame me le aao
df = pd.read_sql(query, conn)

print(df)

print(df.info())
print(df.info())

plt.figure(figsize = (8,10))
plt.bar(df["NAME"], df["LIFETIME_VALUE"] , color="green" , label="TOP CUSTOMERS")
plt.xlabel("name")
plt.ylabel("lifetime_value")
plt.xticks(rotation = 45)
plt.legend(loc="upper center",fontsize=8)
plt.title("TOP 10 CUSTOMERS BY LIFETIME_VALUE")
plt.tight_layout()
plt.savefig("TOP10CUSTOMERS.png")
plt.show()


query = """

SELECT P.PRODUCT_NAME , SUM(TOTAL_AMOUNT) AS TOTAL_SALES , SUM(S.QUANTITY) AS TOTAL_QUANTITY  FROM SALES_D AS S 
JOIN PRODUCTS_DATA AS P
ON P.PRODUCT_ID = S.PRODUCT_ID
GROUP BY P.PRODUCT_NAME
ORDER BY TOTAL_SALES DESC
LIMIT 10;

"""

df = pd.read_sql(query, conn)
print(df)

plt.figure(figsize = (8,10))
plt.barh(df["PRODUCT_NAME"] , df["TOTAL_SALES"], color="pink", label="TOP PRODUCTS")
plt.title("TOP 10 BEST SELLING PRODUCTS")
plt.xlabel("TOTAL_SALES")
plt.ylabel("PRODUCT_NAME")
plt.legend(loc="upper right",fontsize=10)
plt.tight_layout()
plt.savefig("TOP10PRODUCTS.png")

plt.show()


query = """

SELECT 
    DATE_FORMAT(sale_date, '%Y-%m') AS year,
    SUM(total_amount) AS monthly_sales
FROM sales_d
GROUP BY year
ORDER BY year;


"""

df = pd.read_sql(query, conn)
print(df)

plt.figure(figsize = (10,8))
plt.plot(df["year"], df["monthly_sales"] , marker="o" , color="gold" , label="MONTHLY SALES")
plt.title("MONTHLY SALES TREND" , fontweight="bold" , fontsize=12)
plt.xlabel("YEAR_MONTH",fontweight="bold")
plt.ylabel("MONTHLY SALES",fontweight="bold")
plt.legend(loc="upper right",fontsize=10)
plt.xticks(rotation = 50)
plt.tight_layout()
plt.savefig("MONTHLY SALES.png")

plt.show()


query = """

SELECT C.LOCATION, SUM(TOTAL_AMOUNT) AS REVENUE FROM SALES_D AS S
JOIN CUSTOMERS_DATA AS C
ON C.CUSTOMER_ID = S.CUSTOMER_ID
GROUP BY C.LOCATION
ORDER BY REVENUE DESC;

"""

df = pd.read_sql(query, conn)
print(df)

region = df.groupby(["LOCATION"])["REVENUE"].sum()

plt.figure(figsize = (10,8))
plt.pie(region,labels=region.index,autopct="%1.2f%%")
plt.title("REGION WISE REVENUE")
plt.tight_layout()
plt.savefig("REVENUE.png")

plt.show()


query = """

SELECT CATEGORY , SUM(TOTAL_AMOUNT) AS CATEGORY_SALES, 
RANK() OVER(ORDER BY SUM(TOTAL_AMOUNT) DESC) AS SALES_RANK FROM SALES_D AS S
JOIN PRODUCTS_DATA AS P
ON S.PRODUCT_ID = P.PRODUCT_ID
GROUP BY CATEGORY;

"""

df = pd.read_sql(query, conn)
print(df)

plt.figure(figsize = (10,8))
plt.bar(df["CATEGORY"],df["CATEGORY_SALES"],color="skyblue",label="CATEGORY WISE SALES")
plt.title("CATEGORY WISE SALES")
plt.xlabel("CATEGORY",fontweight="bold",fontsize=10)
plt.ylabel("SALES",fontweight="bold",fontsize=10)
plt.legend(loc="upper right",fontsize=10)
plt.tight_layout()
plt.savefig("CATEGORY_WISE.png")

plt.show()

query = """

SELECT YEAR(SALE_DATE)AS YEAR , SUM(TOTAL_AMOUNT) AS SALES_TREND FROM SALES_D
GROUP BY YEAR(SALE_DATE)
ORDER BY YEAR;

"""

df = pd.read_sql(query, conn)
print(df)

plt.figure(figsize = (10,8))
plt.bar(df["YEAR"],df["SALES_TREND"],color="orange",label="SALES TREND")
plt.title("YEARLY PROFIT-LOSS")
plt.xlabel("YEAR",fontweight="bold",fontsize=10)
plt.ylabel("SALES TREND",fontweight="bold",fontsize=10)
plt.legend(loc="upper right",fontsize=10)
plt.tight_layout()
plt.savefig("YEARLY_TREND.png")

plt.show()




