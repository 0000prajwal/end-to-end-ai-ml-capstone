# Query 1: WHERE with comparison operator
# --- Query 1: WHERE filter using a comparison operator ---
q1 = """
SELECT App, Category,  Installs
FROM main_table
WHERE Installs >= 1000000;
"""
df_q1 = pd.read_sql_query(q1, conn)
print("Query 1: Apps with Installs >=  1000000")
display(df_q1.head())


# --- Query 2: WHERE filter using IN and BETWEEN ---

q2 = """
SELECT App, Category, Reviews
FROM main_table
WHERE Category IN ('GAME', 'FAMILY', 'TOOLS')
AND Reviews BETWEEN 1000 AND 50000;
"""

df_q2 = pd.read_sql_query(q2, conn)

print("Query 2: Apps in selected categories with Reviews between 1000 and 50000")
display(df_q2.head())


# ----Query 3: Aggregate function + group by ---
q3 = """
SELECT Category, 
COUNT(*) AS num_apps,
AVG(Reviews) AS avg_reviews,
SUM(Installs) AS max_installs
FROM main_table
GROUP BY Category;
"""

df_q3 = pd.read_sql_query(q3, conn)

print("Query 3: Number of apps, average reviews, and maximum installs by categor")
display(df_q3.head())

# --- Query 4: HAVING clause filtering on aggregated value ---

q4 = """
SELECT Category,
       COUNT(*) AS num_apps,
       AVG(Reviews) AS avg_reviews
FROM main_table
GROUP BY Category
HAVING COUNT(*) > 50
AND AVG(Reviews) > 10000;
"""

df_q4 = pd.read_sql_query(q4, conn)

print("Query 4: Categories with more than 50 apps and average reviews greater than 10000")
display(df_q4.head())

# --- Query 5: ORDER BY + LIMIT ---
q5 = """
SELECT App, Category, Reviews, Installs
FROM main_table
ORDER BY Reviews DESC
LIMIT 10;
"""
df_q5 = pd.read_sql_query(q5, conn)
print("\nQuery 5: Top 10 apps by number of reviews")
display(df_q5.head(10))

# --- Query 6: Multiple WHERE conditions using AND / OR ---

q6 = """
SELECT App, Category, Type, Price, Reviews
FROM main_table
WHERE (Type = 'Free' OR Price = '0')
  AND Reviews >= 10000
  AND Category = 'GAME';
"""

df_q6 = pd.read_sql_query(q6, conn)

print("Query 6: Free games with Reviews >= 10000")
display(df_q6.head())
