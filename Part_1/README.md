\# Google Play Store Data Analysis and Cleaning



\## Project Overview



This project demonstrates an end-to-end data analytics workflow using the Google Play Store dataset. The dataset was explored, cleaned, analyzed using SQL, and visualized using Python. The objective was to improve data quality and generate meaningful insights from the dataset.



---



\## Tools and Libraries Used



\- Python

\- Pandas

\- NumPy

\- Matplotlib

\- SQLite

\- Google Colab



---



\## Dataset Exploration



The following dataset exploration steps were performed:



\- Loaded the dataset using Pandas.

\- Checked dataset shape.

\- Examined data types using `.info()`.

\- Generated summary statistics using `.describe()`.

\- Identified missing values.

\- Identified columns with incorrect data types.



---



\## Missing Values



The following columns contained missing values:



| Column | Handling Method | Reason |

|--------|-----------------|--------|

| Rating | Dropped | 13.6% values were missing (>10% threshold). |

| Type | Filled with Mode | Only one value was missing. |

| Content Rating | Filled with Mode | Only one value was missing. |

| Current Ver | Filled with Mode | Very few missing values. |

| Android Ver | Filled with Mode | Very few missing values. |

| Reviews | Filled with Median | One missing value after numeric conversion. |

| Installs | Filled with Median | One missing value after numeric conversion. |



---



\## Data Type Corrections



The following columns were converted to numeric format:



| Column | Problem | Solution |

|--------|----------|----------|

| Reviews | Stored as text | Converted using `pd.to\_numeric()` |

| Installs | Stored as text with commas and '+' | Removed symbols and converted to numeric |



---



\## Duplicate Rows



\- Removed \*\*483 duplicate rows\*\* using `drop\_duplicates()`.



---



\## Outlier Detection



Outliers were identified using the \*\*Interquartile Range (IQR)\*\* method for numeric columns such as:



\- Reviews

\- Installs



No rows were removed during outlier detection. The analysis was performed only to identify unusual values.



---



\## SQL Analysis



The cleaned dataset was loaded into a SQLite database.



The following SQL operations were performed:



1\. WHERE clause with comparison operator

2\. WHERE using IN and BETWEEN

3\. GROUP BY with AVG()

4\. HAVING clause

5\. ORDER BY with LIMIT

6\. Filtering Free applications



All query results were exported as CSV files.



---



\## Visualizations



The following charts were created:



\- Box Plot (Outlier Check)

\- Histogram

\- Bar Chart using `value\_counts()`

\- Scatter Plot

\- GroupBy Aggregation Bar Chart



Each visualization includes an appropriate title and labelled axes.



---



\# Insights



\- The \*\*Rating\*\* column contained \*\*13.6% missing values\*\*, so it was removed because it exceeded the 10% threshold.

\- A total of \*\*483 duplicate rows\*\* were removed during data cleaning.

\- Only a few missing values existed in \*\*Type\*\*, \*\*Content Rating\*\*, \*\*Current Ver\*\*, and \*\*Android Ver\*\*, so they were filled using the mode.

\- \*\*Reviews\*\* and \*\*Installs\*\* were converted from text to numeric format for analysis and visualization.

\- SQL queries showed that many applications have \*\*more than 1,000,000 installs\*\*, indicating a large number of highly popular apps.

\- The visualizations helped identify outliers in Reviews and compare application categories based on user activity.



---



\## Files Included



\- Google\_Play\_Store\_Project.ipynb

\- README.md

\- googleplaystore.db

\- queries.sql (or SQL notebook cells)

\- query1\_installs\_filter.csv

\- query2\_category\_in\_reviews\_between.csv

\- query3\_groupby\_category.csv

\- query4\_having\_category.csv

\- query5\_top10\_reviews.csv

\- query6\_free\_games\_filter.csv





---



This project was completed by the author using Python, Pandas, NumPy, Matplotlib, SQLite3, and Google Colab.



ChatGPT (OpenAI) was used as a learning and coding assistant to:

\- Understand project requirements.

\- Explain Python, SQL, and data cleaning concepts.

\- Debug code and resolve errors.



\## Conclusion



This project successfully demonstrates a complete data analytics workflow including data exploration, cleaning, SQL querying, and visualization. The cleaned dataset provides reliable insights into Google Play Store applications and satisfies all project requirements.

