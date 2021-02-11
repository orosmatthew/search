# Search

A simple search engine implementation using a Python web crawler, SQL Database, and HTML & PHP webpages.

## Usage

1. Set up an SQL database with 2 tables; websites and connections based on the templates in the "databse_templates" folder
2. Input appropriate values for the hostname, username, password, etc. for the database in the "send_sql_connections.py" and "send_sql_websites.py" scripts in the "python_crawler" folder
3. Run the Python "crawler.py" script to generate lists of websites
4. Run the Python "send_sql_connections.py" and "send_sql_websites.py" scripts to send appropriate data to the SQL database
5. Input appropriate values for the hostname, username, password, etc. for the database in "query.php" in the "web_pages" folder
6. Host the "search.html" and "query.php" scripts on a web server
7. Test it out and tweak your very own search engine!

