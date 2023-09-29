import pandas as pd
import os
import pycountry

def get_language_from_locale(locale):
    try:
        language_code = locale.split('-')[0]
        return pycountry.languages.get(alpha_2=language_code).name
    except AttributeError:
        return locale

dataset_directory = 'C:\\Users\\Admin\\MASSIVE_Data\\amazon_massive_dataset\\data'

"""Read the en-US.jsonl file into a dataframe"""
english_df = pd.read_json(os.path.join(dataset_directory, 'en-US.jsonl'), lines=True)
english_df['en-US'] = english_df['utt'] + ': ' + english_df['annot_utt']

"""Create a new Excel writer object"""
with pd.ExcelWriter('translation_sheets_by_language.xlsx') as writer:

    for filename in os.listdir(dataset_directory):
        if filename.endswith('.jsonl') and filename != 'en-US.jsonl':

            df = pd.read_json(os.path.join(dataset_directory, filename), lines=True)

            locale = df['locale'].iloc[0]
            language_name = get_language_from_locale(locale)

            df[locale] = df['utt'] + ': ' + df['annot_utt']

            merged_df = english_df[['id', 'en-US']].merge(df[['id', locale]], on='id', how='outer')

            merged_df.to_excel(writer, sheet_name=language_name, index=False)