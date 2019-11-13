#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sb
import click

conditioning_qs = {
    'gender': 'What is your primary gender identity (if any)?',
    'age': 'What is your current age?',
    'poc': 'Do you identify as a person of color?',
}

central_qs = {
    'overall_exp': 'How satisfied are you with your overall experience as a Ranger?',
    'appreciated': 'How appreciated do you feel by the Ranger department?',
    'nps': 'If you had a friend that was clearly a Rangerly-type, would you recommend that they volunteer for Rangers?',
    'next_year': 'Do you plan to Ranger at Burning Man in 2020?'
}


def make_bar(central_q, conditioning_q, survey_res, table_row_width_scale=1,
             rotation=0):
    con_res = survey_res.groupby([conditioning_q, central_q]).size().unstack(
        fill_value=0)
    cond_freq_res = con_res.apply(lambda row: row / sum(row), axis=1)

    count_table = con_res.sum(axis=1).apply(str).reset_index()
    count_table_to_display = pd.concat([pd.DataFrame(
        [[count_table.columns[0], "# of Responses"]],
        columns=count_table.columns), count_table])

    long_cond_freq = cond_freq_res.reset_index().melt(
        id_vars=conditioning_q).rename(
        columns={"value": "Fraction of Population"})
    g = sb.catplot(x=central_q, data=long_cond_freq,
                   y='Fraction of Population', col=conditioning_q,
                   kind='bar')
    g.set_titles("{col_var}\n{col_name}")
    g.set_xticklabels(rotation=rotation)
    tbl = plt.table(cellText=count_table_to_display.values,
                    colWidths=[1.1] * len(count_table_to_display.columns),
                    cellLoc='center', rowLoc='center',
                    loc='right')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize('large')
    tbl.scale(table_row_width_scale, 2)


def normalize_genders(df):
    gen_mapping = {'Female': 'f', 'male': 'm', 'Male': 'm', 'Cis Male': 'm',
                   'Male.': 'm', 'female': 'f', 'Man/Male': 'm',
                   'CIS Male': 'm',
                   'Cis male': 'm', 'Male ': 'm', 'Cis-male': 'm', 'M': 'm',
                   'cis-het-male': 'm', 'Man': 'm', 'F': 'f',
                   'Male, definitely': 'm',
                   'man': 'm', 'Dude': 'm', 'woman': 'f',
                   'female / she/her': 'f', 'dude': 'm',
                   'boy': 'm', 'Cisgender Woman': 'f', 'Female ': 'f',
                   "I'm a lady ": 'f', 'Woman': 'f',
                   'Cis-Male': 'm', 'Heteosexual male': 'm',
                   'Cis het male': 'm', 'Him': 'm',
                   'Straight male.': 'm', 'cis-male': 'm', 'he / him': 'm',
                   'Male presenting': 'm', 'male binary': 'm', 'He/Him': 'm',
                   'She/Her': 'f',
                   'slightly male': 'm', 'queer male': 'm', 'maleish': 'm'
                   }
    df['What is your primary gender identity (if any)?\n(Normalized)'] = df[
        'What is your primary gender identity (if any)?'].apply(
        lambda row: gen_mapping.get(row, 'other'))
    return df


@click.command()
@click.option('--input_data', help='The file path to csv file containing '
                                   'survey data.')
def main(input_data):
    survey_res = pd.read_csv(input_data)

    # * How satisfied are you with your overall experience as a Ranger?
    make_bar('How satisfied are you with your overall experience as a Ranger?',
             'Did you Ranger at Burning Man in 2019?',
             survey_res)
    plt.savefig(
        'img/overall_exp_cond_on_ranger_this_year.png',
        bbox_inches="tight", pad_inches=1)

    rangered_2019 = survey_res[
        survey_res['Did you Ranger at Burning Man in 2019?'] == 'Yes']
    rangered_2019 = normalize_genders(rangered_2019)

    make_bar('How included do you feel in the Rangers?',
             'Do you identify as a person of color?', rangered_2019)
    plt.savefig(
        'img/how_included_cond_on_poc_filtered_by_ranger_2019.png',
        bbox_inches="tight", pad_inches=1)


if __name__ == '__main__':
    main()
