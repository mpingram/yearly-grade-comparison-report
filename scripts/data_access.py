import pandas as pd


def get_grade_df(filepath):

    df = pd.read_csv(filepath)

    # add column with ClassName (SubjectName + StudentHomeroom)
    df["ClassName"] = df.apply(lambda row:
            "{} ({})".format(row.loc["SubjectName"], row.loc["StudentHomeroom"]), axis=1)

    return df
