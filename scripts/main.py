import pandas as pd
import numpy as np

import gradeutils
from data_access import get_grade_df

def calc_gpa(*args):
    # FIXME: I'm 95% sure this is accurate -- need to confirm.
    sum = 0
    n = len(args)
    for grade in args:

        if np.isnan(grade):
            return np.nan 

        lettergrade = gradeutils.to_letter_grade(grade, 100)
        if lettergrade == "A":
            sum += 4.0
        elif lettergrade == "B":
            sum += 3.0
        elif lettergrade == "C":
            sum += 2.0
        elif lettergrade == "D":
            sum += 1.0
        elif lettergrade == "F":
            sum += 0.0
        else:
            raise ValueError("Unknown letter grade: {}".format(lettergrade))

    return sum/float(n)

def aggregate_grades(grade_df):
    aggregated_df_proto = []
    grade_gdf_by_id = grade_df.groupby("StudentID")

    def get_grade(df, subj_name):
        try:
            grade_series = df[df["SubjectName"] == subj_name]["FinalAvg"]
            return grade_series.iloc[0]
        except IndexError:
            return np.nan

    for student_id, df in grade_gdf_by_id:

        math_grade = get_grade(df, "MATHEMATICS STD")
        read_grade = get_grade(df, "CHGO READING FRMWK")
        sci_grade = get_grade(df, "SCIENCE  STANDARDS")
        soc_sci_grade = get_grade(df, "SOCIAL SCIENCE STD")

        print([math_grade, read_grade, sci_grade, soc_sci_grade])

        gpa = calc_gpa(math_grade, read_grade, sci_grade, soc_sci_grade)


        aggregated_df_proto.append({
            "StudentID": student_id,
            "StudentFirstName": df.iloc[0]["StudentFirstName"],
            "StudentLastName": df.iloc[0]["StudentLastName"],
            "StudentHomeroom": df.iloc[0]["StudentHomeroom"],

            "Math_Avg": math_grade,
            "Reading_Avg": read_grade,
            "Science_Avg": sci_grade,
            "Social_Science_Avg": soc_sci_grade,
            "GPA": gpa
        })

    return pd.DataFrame(aggregated_df_proto)

def create_grade_comparison_df(**kwargs):
    ly_grades = kwargs.get("ly", None)
    cy_grades = kwargs.get("cy", None)
    if ly_grades is None or cy_grades is None:
        raise ValueError("ly or cy kwargs not passed to merge_aggregated_grades. Instead got: {}".format(kwargs))

    # merge dfs on StudentID, ignoring LY records where
    # no matching StudentID found (via "how='left'")
    print(len(cy_grades), len(ly_grades))
    grade_comparison_df = pd.merge(cy_grades, ly_grades, on="StudentID", suffixes=["_CY", "_LY"])

    print(grade_comparison_df.columns)

    # drop StudentFirstName_ly, StudentLastName_ly, StudentHomeroom_ly
    grade_comparison_df = grade_comparison_df.drop([
        "StudentFirstName_LY", 
        "StudentLastName_LY", 
        "StudentHomeroom_LY"
        ], axis=1)

    # remove suffix from StudentFirstName_cy, StudentLastName_cy, StudentHomeroom_cy
    grade_comparison_df = grade_comparison_df.rename(columns={
        "StudentFirstName_CY": "StudentFirstName",
        "StudentLastName_CY": "StudentLastName",
        "StudentHomeroom_CY": "StudentHomeroom",
        })

    # add grade change columns for each grade
    grade_comparison_df = grade_comparison_df.assign(
            Math_change=grade_comparison_df["Math_Avg_CY"] - grade_comparison_df["Math_Avg_LY"],
            Reading_change=grade_comparison_df["Reading_Avg_CY"] - grade_comparison_df["Reading_Avg_LY"],
            Science_change=grade_comparison_df["Science_Avg_CY"] - grade_comparison_df["Science_Avg_LY"],
            Social_Science_change=grade_comparison_df["Social_Science_Avg_CY"] - grade_comparison_df["Social_Science_Avg_LY"],
            GPA_change=grade_comparison_df["GPA_CY"] - grade_comparison_df["GPA_LY"]
        )

    # set StudentID as index
    grade_comparison_df.set_index("StudentID", inplace=True)

    # reorder columns
    grade_comparison_df = grade_comparison_df[[
        "StudentLastName", 
        "StudentFirstName",
        "StudentHomeroom",
        "Math_Avg_LY",
        "Math_Avg_CY",
        "Math_change",
        "Reading_Avg_LY",
        "Reading_Avg_CY",
        "Reading_change",
        "Science_Avg_LY",
        "Science_Avg_CY",
        "Science_change",
        "Social_Science_Avg_LY",
        "Social_Science_Avg_CY",
        "Social_Science_change",
        "GPA_LY",
        "GPA_CY",
        "GPA_change",
    ]]

    return grade_comparison_df

def main():
    LY_GRADES_FILEPATH = "../data/ly_grades.csv"
    CY_GRADES_FILEPATH = "../data/cy_grades.csv"

    OUTPUT_FILENAME = "../reports/grade_comparison_report.xlsx"

    ly_grades_df = get_grade_df(LY_GRADES_FILEPATH)
    cy_grades_df = get_grade_df(CY_GRADES_FILEPATH)

    # aggregate both last year's grades and current year grades on StudentID,
    # transforming dfs into form StudentID, StudentName, StudentHomeroom, MathGrade, ReadGrade, SciGrade, SocSciGrade, GPA
    ly_aggregated_grades = aggregate_grades(ly_grades_df)
    cy_aggregated_grades = aggregate_grades(cy_grades_df)
   
   # # index dfs on StudentID, which (should) be unique now
   # ly_aggregated_grades.set_index("StudentID", inplace=True)
   # cy_aggregated_grades.set_index("StudentID", inplace=True)

    # create grade_comparison_df, with fields
    # StudentID, StudentFirstName, StudentLastNAme, StudentHomeroom, [grade]_Avg_LY, [grade]_Avg_CY, [grade]_change, GPA_LY, GPA_CY, GPA_change
    # where [grade] is one of 'Math', 'Reading', 'Science', 'Social Science'
    grade_comparison_df = create_grade_comparison_df(cy=cy_aggregated_grades, ly=ly_aggregated_grades)

    # group grade_comparison_df on Homeroom
    grade_comparison_gdf_by_homeroom = grade_comparison_df.groupby("StudentHomeroom")

    # write to XLSX -- each group gets its own sheet
    writer = pd.ExcelWriter(OUTPUT_FILENAME)
    for homeroom, df in grade_comparison_gdf_by_homeroom:
        df.to_excel(writer, sheet_name=homeroom)

    writer.save()
    # ta-da!

if __name__ == "__main__":
    main()
