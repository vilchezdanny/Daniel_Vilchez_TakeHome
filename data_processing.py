import re
import pandas as pd
from IPython.display import display_html


def explore_null_values(df):
    """
    returns a dataframe with the number of missing values, percent of missing values, and the column data type
    """
    # null counts
    null_counts = df.isnull().sum()

    # null percentage
    null_pct = round((null_counts / df.shape[0] * 100), 0)
    null_pct = null_pct.astype(int).astype(str) + "%"

    # create a df using counts and pct
    null_df = pd.DataFrame({"null_counts": null_counts, "null_pct": null_pct})
    null_df["data_types"] = df.dtypes
    null_df = null_df.sort_index()

    return null_df


def drop_unnecessary_columns(df):
    df.drop(
        [
            "Unnamed: 0",
            "id",
            "url",
            "region_url",
            "region",
            "condition",  # dropping because there are too many missing values
            "title_status",
            "model",
            "vin",
            "size",  # dropping because there are too many missing values
            "paint_color",
            "image_url",
            "county",  # dropping because there are too many missing values
            "size",
            "lat",
            "long",
        ],
        axis=1,
        inplace=True,
    )


def clean_year_column(df):
    """
    Uses regex to find year in description to fill missing values in year column and cast to datetime
    """
    df["description_year"] = df["description"].str.extract(
        r"([1-2][0][0-2][1-9])", expand=False
    )
    df["year"].fillna(df["description_year"], inplace=True)
    df.drop(["description_year"], axis=1, inplace=True)
    df["year"].dropna(inplace=True)
    df["year"] = df["year"].astype(int)


def clean_cylinder_strings(df):
    """
    Cleans cylinder column by removing all non-numeric characters
    """
    df["cylinders"] = df["cylinders"].str.strip().str.split(" ").str[0]
    df = df[df["cylinders"] != "other"]


def find_cylinders_in_description(df):
    """
    Uses regex to find number of cylinders in description to fill missing values in cylinders column
    """
    df["description_cylinder"] = df["description"].str.extract(
        r"([vV]-?[0-9])", expand=False
    )
    df["description_cylinder"] = (
        df["description_cylinder"].str.lower().str.replace("v", "").str.replace("-", "")
    )
    df["cylinders"].fillna(df["description_cylinder"], inplace=True)
    df.drop(["description_cylinder"], axis=1, inplace=True)


def search_description_for_cylinders(df):
    """
    Uses another regex method to find the cylinders in the description
    """
    df["description_cylinder_1"] = df["description"].str.extract(
        r"([0-9](?= cylinders))", expand=False
    )
    df["description_cylinder_2"] = df["description"].str.extract(
        r"([0-9](?= cylinder))", expand=False
    )
    df["description_cylinder_3"] = df["description"].str.extract(
        r"((?<=cylinders )[0-9])", expand=False
    )
    df["description_cylinder_4"] = df["description"].str.extract(
        r"((?<=cylinder )[0-9])", expand=False
    )

    df["cylinders"].fillna(df["description_cylinder_1"], inplace=True)
    df["cylinders"].fillna(df["description_cylinder_2"], inplace=True)
    df["cylinders"].fillna(df["description_cylinder_3"], inplace=True)
    df["cylinders"].fillna(df["description_cylinder_4"], inplace=True)

    df.drop(
        [
            "description_cylinder_1",
            "description_cylinder_2",
            "description_cylinder_3",
            "description_cylinder_4",
        ],
        axis=1,
        inplace=True,
    )


def remove_odd_cylinders(df):
    """
    removes cylinder numbers that are not likely to be real car cylinders
    """
    df["cylinders"] = df.loc[
        df["cylinders"].isin(["4", "6", "8", "10", "12"]), "cylinders"
    ]


def clean_cylinder_column(df):
    """
    performs all the cleaning functions on the cylinders column for readability in jupyter notebook
    """
    clean_cylinder_strings(df)
    find_cylinders_in_description(df)
    search_description_for_cylinders(df)
    remove_odd_cylinders(df)


def find_type_in_description(df):
    """
    Uses regex to find car type in description to fill missing values in condition column
    """
    df["description_type"] = (
        df["description"]
        .str.extract(
            r"(SUV|sedan|pick-up|coupe|truck|convertible|hatchback|van|wagon|mini-van|offroad)",
            expand=False,
            flags=re.I,
        )
        .str.lower()
    )
    df["type"].fillna(df["description_type"], inplace=True)
    df.drop(["description_type"], axis=1, inplace=True)


def clean_type_column(df):
    """
    compiles all cleaning functions for the type column for readability in jupyter notebook
    """
    df["type"] = df["type"].str.lower()
    find_type_in_description(df)


COLUMNS = [
    "price",
    "year",
    "manufacturer",
    "cylinders",
    "fuel",
    "odometer",
    "transmission",
    "drive",
    "type",
    "state",
]


def display_null_dataframes_side_by_side(df1, df2):
    df = df1[COLUMNS]
    df1 = explore_null_values(df)
    df2 = explore_null_values(df2)
    df_1_styler = df1.style.set_table_attributes("style='display:inline'").set_caption(
        "craigslist_raw_null_values"
    )
    df_2_styler = df2.style.set_table_attributes("style='display:inline'").set_caption(
        "craigslist_null_values"
    )

    display_html(df_1_styler._repr_html_() + df_2_styler._repr_html_(), raw=True)


def drop_low_pct_missing_values(df):
    df.dropna(subset=["fuel", "manufacturer", "transmission"], inplace=True)


def impute_odometer_with_median(df):
    df["odometer"].fillna(df["odometer"].median(), inplace=True)
    df["odometer"] = df["odometer"].astype(int)


def impute_cylinders_with_mode(df):
    df.loc[df["manufacturer"] == "tesla", "cylinders"] = 0
    df["cylinders"] = df.groupby("manufacturer")["cylinders"].apply(
        lambda x: x.fillna(x.mode().iloc[0])
    )
    df["cylinders"] = df["cylinders"].astype(int)


def impute_drive_with_mode(df):
    df["drive"] = df.groupby("manufacturer")["drive"].apply(
        lambda x: x.fillna(x.mode().iloc[0])
    )


def impute_type_with_mode(df):
    df["type"] = df.groupby("manufacturer")["type"].apply(
        lambda x: x.fillna(x.mode().iloc[0])
    )
