# gsmarena.com

Web scraper that pull data from gsmarena.com


Installation
------------

You can create a virtual environment and install the required packages with the following commands:
```bash
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Usage:
-------

```bash
$ scrapy crawl gsmarena_spider --set FEED_URI=output.json --set FEED_FORMAT=json
```
__