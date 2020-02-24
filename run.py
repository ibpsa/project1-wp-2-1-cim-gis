#!/usr/bin/python

import os
import re
import sys

import pandas as pd
from jinja2 import Environment, PackageLoader
from markdown2 import markdown_path


def print_usage():
    print("Usage: {} file [file ...] path".format(sys.argv[0]))
    quit(-1)


def df_to_html_table(df: pd.DataFrame):
    return df.to_html(render_links=True, classes=['mdl-data-table', 'mdl-js-data-table', 'mdl-shadow--2dp'])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()

    infiles = sys.argv[1:-1]
    outpath = sys.argv[-1]

    if not os.path.exists(outpath):
        os.mkdir(outpath)

    env = Environment(
        loader=PackageLoader('app', 'templates')
    )
    template = env.get_template('base.html')

    countries = []
    for infile in infiles:
        country = re.sub('\\..+$', '', os.path.basename(infile))
        outfile = country + '.html'
        countries.append({'name': country.capitalize(), 'infile': infile, 'outfile': outfile})

    for country in countries:
        df = pd.read_csv(country['infile'])
        df = df.drop(columns=['Description', 'Use', 'Type'])

        with open(os.path.join(outpath, country['outfile']), 'w') as file:
            file.write(template.render(content=df_to_html_table(df), title=country['name'], countries=countries))

    md = markdown_path('content/Categories.md')
    df = pd.read_csv("content/categories.csv")
    with open(os.path.join(outpath, 'categories.html'), 'w') as file:
        file.write(template.render(content=md + df_to_html_table(df), title='Data categories', countries=countries))

    md_files = [
        ('Home', 'content/Home.md', 'index.html'),
        ('Contribute', 'content/Contribute.md', 'contribute.html'),
        ('Links', 'content/Links.md', 'links.html')
    ]

    for title, in_file, out_file in md_files:
        md = markdown_path(in_file)
        with open(os.path.join(outpath, out_file), 'w') as file:
            file.write(template.render(content=md, title=title, countries=countries))
