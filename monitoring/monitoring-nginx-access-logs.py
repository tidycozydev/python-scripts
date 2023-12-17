import argparse, datetime, pandas

# Arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--ips", help="IPs we don't need to monitor, comma-separated values")
args = argParser.parse_args()


access_log = open('/var/log/nginx/access.log', 'r')

# Find this line of code here: https://riptutorial.com/pandas/example/15180/read-nginx-access-log--multiple-quotechars-
# Find the regex here: https://linuxtech.in/efficiently-parsing-nginx-log-files-using-python/
df = pandas.read_csv(
        access_log,
        sep=r'(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"',
        engine='python',
        usecols=[1, 2, 3, 4, 5, 6, 7],
        names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
        na_values='-',
        header=None)

# Filter IP addresses we don't care about and query for non 200 response status
ipsToIgnore = args.ips.split(',')
filtered_df = df[~df['ip'].isin(ipsToIgnore)].query('status != 200')

# Group by IPs and status, add a count column, sort
html_df = filtered_df.groupby(['ip', 'status'])['status'].count().sort_values(ascending=False).reset_index(name='count')

# Filter requests trying to access some .env file
csv_df = filtered_df[filtered_df['request'].str.contains('.env')]


date_str = datetime.datetime.now().strftime("%Y-%m-%d")

# Write a file containing all the suspect IPs for manual monitoring
html_file = open('html/table-' + date_str + '.html', 'w')
html_file.write(html_df.to_html())

# Write a file containing all the suspects IPs for automated usages
csv_file = open('csv/ips-' + date_str + '.csv', 'w')
csv_file.write(csv_df.drop_duplicates(subset = 'ip')['ip'].to_csv(index=False))
