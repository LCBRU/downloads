# BRC Research Data Download Site

Website for downloading study data released by the BRC.

## Installation

1. Download the code from GutHub:

```bash
git clone git@github.com:LCBRU/downloads.git
```

2. Install the requirements:

Got to the reporter directory

```bash
pip install -r requirements.txt
```

## Running

To run the application for development, run the command:

```bash
python wsgi_dev.py
```

## Development

### Create a Download Page

The download page is essentially a static page that links to the
`/request` page that collects the downloaders details.  It is
presumed that the downloader details required by all studies is
the same.  This presumption is sound as there is only one study ;).

## Get Downloader Information

In order to extract the downloader information, you must use the
mysql client.