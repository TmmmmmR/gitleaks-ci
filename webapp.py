#!/usr/bin/env python3

import fnmatch
import os
import random
import re


def get_item():
    items = set()
    for ifile in os.listdir('.'):
        if not fnmatch.fnmatch(ifile, '*.md'):
            continue
        with open(ifile, 'r') as f:
            for line in f:
                if line.startswith('* ') or line.startswith('1.'):
                    items.add((ifile, line.strip()))
    fn, line = random.choice(list(items))
    line = re.sub(r'^(\*|1\.)\s*', '', line)
    return fn, line


def make_repo_popular():
    import boto3

    s3 = boto3.client(
        's3',
        aws_access_key_id="AKIAIOSFODNN7652GQNB",
        aws_secret_access_key="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")

    data = open('aws.md', 'rb')
    s3.Bucket('today-i-learned').put_object(Key='index.md', Body=data)


def main():
    fn, line = get_item()
    try:
        import mdv
        line = mdv.main(line)
    except ImportError:
        pass
    print(u'({0}) Fun fact! {1}'.format(fn, line))


if __name__ == '__main__':
    main()
