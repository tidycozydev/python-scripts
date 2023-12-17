import argparse, pandas

# Arguments
argParser =  argparse.ArgumentParser()
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
sub_df = df[~df['ip'].isin(ipsToIgnore)].query('status != 200')

# Group by IPs and status, add a count column, order
new_df = sub_df.groupby(['ip', 'status'])['status'].count().sort_values(ascending=False).reset_index(name='count')

# Print in HTML format
print(new_df.to_html())
