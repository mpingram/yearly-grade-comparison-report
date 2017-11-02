# [CPS Reports] Yearly grade comparison report

## Purpose:
  Compare last year and current year average grades for each student, 
  broken down by category.

## Description
  Takes in previous year and current year Gradebook data. Generates an excel file with a new sheet for each homeroom displaying:
    * GPA
      ..* last year Q4 GPA
      ..* current year (most recent quarter) GPA
      ..* last year to current year GPA change 

    * Reading grades
      ..* last year Q4 Reading grade
      ..* current year (most recent quarter) Reading grade 
      ..* last year to current year GPA change 

    * Math grades
      ..* last year Q4 Math grade
      ..* current year (most recent quarter) Math grade 
      ..* last year to current year GPA change 
    
    * Science grades
      ..* last year Q4 Science grade
      ..* current year (most recent quarter) Science grade 
      ..* last year to current year GPA change 

    * Social Science grades
      ..* last year Q4 Social Science grade
      ..* current year (most recent quarter) Social Science grade 
      ..* last year to current year GPA change 

## Source files:
  * current student quarterly grade averages
    ..* Gradebook -> reports -> ES Cumulative Grades Extract (download as .csv)
      -> save as "./data/current-year-es-cumulative-grades-extract/[any filename].csv"
  * last year's student quarterly grade averages (*Grades from >1 year ago cannot be downloaded from Gradebook* -- must have a copy on hand.)
    ..* [local copy of EC Cumulative Grades Extract from Q4 previous year] 
      -> save as "./data/last-year-es-cumulative-grades-extract/[any filename].csv"

## Output:
  Saves one .xlsx report, with one sheet for each homeroom, to the reports/ folder. 

## Language:
  * python == 3.6

# Dependencies:
  * pandas == 0.21.0
  * openpyxl == 2.4.9
  * numpy == 1.13.03
