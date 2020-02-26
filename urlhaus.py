#!/usr/bin/env python

# https://github.com/ranguli/urlhaus.py
# A simple script to submit URLs to URLhaus either in bulk from a file, or
# individually. Inspired by https://github.com/cocaman/urlhaus/

import re
import sys
from pprint import PrettyPrinter
from urllib.parse import urlsplit, urlunsplit

import requests
import click

from decouple import config

api_url = "https://urlhaus.abuse.ch/api/"
API_KEY = config("API_KEY")


def validate(item, *, validator):
    valid = False

    if validator == "" or not validator:
        return
    elif validator == "url":
        expression = re.compile(
            "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"
        )
    elif validator == "tag":
        expression = re.compile(r'([A-Za-z0-9.-]+)')

    match = re.match(expression, item)

    if match is None:
        valid = False

    elif match:
        valid = True

    return valid


@click.command()
@click.option("-a", "--anon", "anon", flag_value="anon", default=False)
@click.option("-p", "--preview-only", "preview_only", flag_value="preview_only", default=False)
@click.option("-u", "--url", help="The URL to submit")
@click.option("-f", "--file", "file_", help="A file containing URLs to submit")
@click.option(
    "-t", "--tags", help="A tag for your submission (comma seperated if multiple)"
)
def main(url, file_, anon, preview_only, tags):

    submissions = []
    submit_tags = []

    if not file_ and not url:
        sys.exit("You must supply either --url or --file")

    if anon and not isinstance(anon, bool):
        sys.exit("Anonymous value must be true/false")

    if tags:
        if "," in tags and isinstance(tags.split(","), list):
            tags = tags.split(",")
            for tag in tags:
                if tag == "" or not validate(tag, validator="tag"):
                    print("Tag {tag} was invalid, not using it.".format(tag=tag))
                else:
                    submit_tags.append(tag)
        elif tags != "" and validate(tags, validator="tag"):
            submit_tags.append(tags)


    if file_:
        with open(file_, "r") as f:
            urls = f.read().split("\n")
            for url in urls:
                if validate(url, validator="url"):
                    if not url.startswith("https://www."):
                        url = "https://www." + url
                    submissions.append(
                        {"url": url, "threat": "malware_download", "tags":
                            submit_tags,}
                    )
                else:
                    pass

    if url:
        if validate(url, validator="url"):
            submissions.append(
                {"url": url, "threat": "malware_download", "tags": submit_tags,}
            )
        else:
            print("Invalid URL {url}, not going to submit it".format(url=url))
            pass

    if anon:
        anon = 1
    else:
        anon = 0

    json_data = {"token": API_KEY, "anonymous": anon, "submission": submissions}
    headers = {"Content-Type": "application/json"}

    if not json_data.get("submission"):
        sys.exit("No submission data!")

    if preview_only:
        print_data = json_data
        print_data["token"] = "****"

        pp = PrettyPrinter()
        pp.pprint(print_data)
    else:
        r = requests.post(api_url, json=json_data, timeout=15, headers=headers)
        print("Submission status: \n" + r.text)


if __name__ == "__main__":
    main()
