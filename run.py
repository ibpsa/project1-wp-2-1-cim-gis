#!/usr/bin/python

import os
import re
import sys

import pandas as pd
from jinja2 import Environment, PackageLoader


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
    template = env.get_template('template.html')

    countries = []
    for infile in infiles:
        country = re.sub('\\..+$', '', os.path.basename(infile))
        outfile = country + '.html'
        countries.append({'name': country.capitalize(), 'infile': infile, 'outfile': outfile})

    for country in countries:
        df = pd.read_csv(country['infile'])
        df = df.drop(columns=['Description', 'Use', 'Type'])

        with open(os.path.join(outpath, country['outfile']), 'w') as file:
            file.write(template.render(table=df_to_html_table(df), title=country['name'], countries=countries))

    df = pd.read_csv('template.csv')
    with open(os.path.join(outpath, 'index.html'), 'w') as file:
        file.write(template.render(table=df_to_html_table(df), title='Description', countries=countries))
