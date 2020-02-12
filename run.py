#!/usr/bin/python

import os
import re
import sys

import pandas as pd
from html_writer import Html


def print_usage():
    print("Usage: {} file [file ...] path".format(sys.argv[0]))
    quit(-1)


def df_to_html_table(df: pd.DataFrame, html: Html):
    html += df.to_html(render_links=True, classes=['mdl-data-table', 'mdl-js-data-table', 'mdl-shadow--2dp'])


style = """
<style>
   .mdl-data-table {white-space: unset;}
</style>
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()

    infiles = sys.argv[1:-1]
    outpath = sys.argv[-1]

    if not os.path.exists(outpath):
        os.mkdir(outpath)

    header = """<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
    <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>""" + style

    countries = []
    for infile in infiles:
        country = re.sub('\\..+$', '', os.path.basename(infile))
        countries.append(country)

    for infile in infiles:
        country = re.sub('\\..+$', '', os.path.basename(infile))
        df = pd.read_csv(infile)
        df = df.drop(columns=['Description', 'Use', 'Type'])

        html = Html()
        with html.tag('html'):
            with html.tag('div', classes=['mdl-layout', 'mdl-js-layout', 'mdl-layout--fixed-drawer']):
                with html.tag('div', classes=["mdl-layout__drawer"]):
                    html += '<span class="mdl-layout-title">Countries</span>'
                    with html.tag('nav', classes=['mdl-navigation']):
                        for c in countries:
                            html += '<a class="mdl-navigation__link" href="{}">{}</a>'.format(c + '.html',
                                                                                              c.capitalize())
                with html.tag('header', classes=['mdl-layout__header']) as h:
                    h += header
                    with html.tag('div', classes=['mdl-layout__header-row']):
                        with html.tag('span', classes=['mdl-layout-title']) as t:
                            t += country.capitalize()
                with html.tag('div', classes=['mdl-grid']):
                    df_to_html_table(df, html)

        with open(os.path.join(outpath, country + '.html'), 'w') as file:
            file.write(html.to_raw_html())

    html = Html()
    with html.tag('html'):
        html += header
        with html.tag('div', classes=['mdl-layout', 'mdl-js-layout', 'mdl-layout--fixed-drawer']):
            with html.tag('div', classes=["mdl-layout__drawer"]):
                html += '<span class="mdl-layout-title">Countries</span>'
                with html.tag('nav', classes=['mdl-navigation']):
                    for country in countries:
                        html += '<a class="mdl-navigation__link" href="{}">{}</a>'.format(country + '.html',
                                                                                          country.capitalize())
            with html.tag('header', classes=['mdl-layout__header']) as h:
                with html.tag('div', classes=['mdl-layout__header-row']):
                    with html.tag('span', classes=['mdl-layout-title']) as t:
                        t += 'Description'
            with html.tag('main', classes=['mdl-layout__content']):
                with html.tag('div', classes=['mdl-grid']):
                    df = pd.read_csv('template.csv')
                    df_to_html_table(df, html)

    with open(os.path.join(outpath, 'index.html'), 'w') as file:
        file.write(html.to_raw_html())
