# urlhaus.py

urlhaus.py is a simple, quick and dirty script for submitting a malicious URL
to [URLhaus](https://urlhaus.abuse.ch) using the [URLhaus API](https://urlhaus-api.abuse.ch/).


## Usage:

```
python3 urlhaus.py --help

Options:
  -a, --anon
  -p, --preview-only
  -u, --url TEXT      The URL to submit
  -f, --file TEXT     A file containing URLs to submit
  -t, --tags TEXT     A tag for your submission (comma seperated if multiple)
  --help              Show this message and exit.
```

### Submit a URL to URLhaus

```
python3 urlhaus.py -u https://evilurl.com -t phishing,spam,malware
```

### Bulk submit URLs to URLhaus from a file

```
python3 urlhaus.py -f baddies.txt -t phishing,spam,malware
```

### Perform a dry run to inspect the data you are about to send

```
python3 urlhaus.py --url https://evilurl.com --preview-only --tags phishing,malware,spam

{'anonymous': 0,
 'submission': [{'tags': ['phishing', 'malware', 'spam'],
                 'threat': 'malware_download',
                 'url': 'https://evilurl.com'}],
 'token': '****'}
```
