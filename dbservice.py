import os
import psycopg2
import urlparse
conn=None
try:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

except:
    conn=psycopg2.connect(
    database='d5609lnofai4bf',
    user='ifsrjsjivniswq',
    password='aee97ad05b63cf9fcd2f5e56a3bddc56afa0c0283c497598a4576ecc4e1d7f9a',
    port='5432',
    host='ec2-23-23-92-179.compute-1.amazonaws.com'
    )
