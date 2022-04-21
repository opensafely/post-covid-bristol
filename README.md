# post-covid-bristol

This is the code and configuration for post-covid-bristol.

You can run this project via [Gitpod](https://gitpod.io) in a web browser by clicking on this badge: [![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/opensafely/post-covid-bristol)

* The methods and results of this work are summarized below
* Raw model outputs, including charts, crosstabs, etc, are in `released_outputs/`
* If you are interested in how we defined our variables, take a look at the [study definition](analysis/study_definition.py); this is written in `python`, but non-programmers should be able to understand what is going on there
* If you are interested in how we defined our code lists, look in the [codelists folder](./codelists/).
* Developers and epidemiologists interested in the framework should review [the OpenSAFELY documentation](https://docs.opensafely.org)

# About the OpenSAFELY framework

The OpenSAFELY framework is a Trusted Research Environment (TRE) for electronic
health records research in the NHS, with a focus on public accountability and
research quality.

Read more at [OpenSAFELY.org](https://opensafely.org).

# Licences
As standard, research projects have a MIT license. 

# Methods

## Population

All individuals aged 18 and over, who were registered at a TPP practice for a year or more prior to index date.

## COVID-19 diagnosis

COVID-19 diagnosis was defined as a record of a positive COVID-19 polymerase chain reaction (PCR), or antigen test, or a confirmed COVID-19 diagnosis in primary care or secondary care hospital admission records or on the death registry and derived as the earliest date on which COVID-19 was recorded.

## Outcomes

Outcomes were defined using primary care, hospital admission and national death registry data. Specialist clinician-verified SNOMED-CT and ICD-10 rule-based phenotyping algorithms were used to define fatal or non-fatal myocardial infarction (MI).

## Potential confounding variables

Primary and secondary care records up to 1st January 2020 were used to define ethnicity, deprivation, smoking status and region. A large number of potentially confounding variables were defined based on previous disease diagnoses, comorbidities and medications.

## Statistical Analyses

Hazard ratios (HRs) were estimated for time since diagnosis of COVID-19 (categorised as 0-6 days, 1-2 weeks, 3-4, 5-8, 9-12, 13-26 and 27-49 weeks since diagnosis), compared with follow up without or before diagnosis of COVID-19 (reference group). Analyses used Cox regression models with calendar time scale (starting on 1st January 2020), to account for rapid changes in incidence rates during the pandemic, fitted separately by age group (categorised as <40, 40-59, 60-79 and ≥80 years on 1st January 2020) and by population (England and Wales). Censoring was at the earliest of the date of the outcome, death, or 7th December 2020 (the day before the UK COVID-19 vaccine rollout started). For computational efficiency, analyses included all people with the outcome of interest or with a record of COVID-infection, and a 10% randomly sampled subset of other people. Analyses incorporated inverse probability weights with robust standard errors to account for this sampling. Overall HRs were combined across age groups using inverse-variance weighted meta-analyses. Crude and maximally adjusted HRs were estimated: the latter controlled for all the potential confounders.

# Results

| model              | sex   | week  | estimate | std.error | robust.se | conf.low | conf.high | statistic | p.value  |
|--------------------|-------|-------|----------|-----------|-----------|----------|-----------|-----------|----------|
| Crude              | All   | 1     | 62.24    | 0.03      | 0.03      | 58.51    | 66.21     | 131.07    | 0.00E+00 |
| Crude              | All   | 2     | 5.37     | 0.10      | 0.10      | 4.37     | 6.59      | 16.04     | 6.77E-58 |
| Crude              | All   | 3-4   | 3.27     | 0.10      | 0.10      | 2.68     | 3.99      | 11.72     | 1.03E-31 |
| Crude              | All   | 5-8   | 2.26     | 0.11      | 0.11      | 1.83     | 2.78      | 7.67      | 1.72E-14 |
| Crude              | All   | 9-12  | 3.03     | 0.12      | 0.12      | 2.38     | 3.85      | 9.06      | 1.32E-19 |
| Crude              | All   | 13-26 | 3.14     | 0.08      | 0.08      | 2.69     | 3.67      | 14.32     | 1.71E-46 |
| Crude              | All   | 27-49 | 2.99     | 0.14      | 0.14      | 2.28     | 3.93      | 7.87      | 3.58E-15 |
| Maximally adjusted | All   | 1     | 46.67    | 0.03      | 0.03      | 43.88    | 49.64     | 122.20    | 0.00E+00 |
| Maximally adjusted | All   | 2     | 4.25     | 0.10      | 0.10      | 3.46     | 5.22      | 13.82     | 2.03E-43 |
| Maximally adjusted | All   | 3-4   | 2.69     | 0.10      | 0.10      | 2.20     | 3.27      | 9.78      | 1.39E-22 |
| Maximally adjusted | All   | 5-8   | 1.72     | 0.11      | 0.11      | 1.40     | 2.12      | 5.14      | 2.78E-07 |
| Maximally adjusted | All   | 9-12  | 1.81     | 0.12      | 0.12      | 1.42     | 2.30      | 4.84      | 1.31E-06 |
| Maximally adjusted | All   | 13-26 | 1.54     | 0.08      | 0.08      | 1.32     | 1.81      | 5.41      | 6.36E-08 |
| Maximally adjusted | All   | 27-49 | 1.29     | 0.14      | 0.14      | 0.98     | 1.70      | 1.84      | 6.61E-02 |
| Maximally adjusted | Men   | 1     | 48.65    | 0.04      | 0.04      | 45.02    | 52.56     | 98.37     | 0.00E+00 |
| Maximally adjusted | Men   | 2     | 4.19     | 0.14      | 0.14      | 3.21     | 5.46      | 10.58     | 3.75E-26 |
| Maximally adjusted | Men   | 3-4   | 2.77     | 0.13      | 0.13      | 2.16     | 3.56      | 7.99      | 1.40E-15 |
| Maximally adjusted | Men   | 5-8   | 1.73     | 0.14      | 0.14      | 1.33     | 2.26      | 4.02      | 5.72E-05 |
| Maximally adjusted | Men   | 9-12  | 1.94     | 0.16      | 0.16      | 1.43     | 2.64      | 4.24      | 2.28E-05 |
| Maximally adjusted | Men   | 13-26 | 1.41     | 0.11      | 0.11      | 1.14     | 1.76      | 3.10      | 1.95E-03 |
| Maximally adjusted | Men   | 27-49 | 1.37     | 0.18      | 0.18      | 0.97     | 1.95      | 1.78      | 7.43E-02 |
| Maximally adjusted | Women | 1     | 43.45    | 0.05      | 0.05      | 39.24    | 48.11     | 72.57     | 0.00E+00 |
| Maximally adjusted | Women | 2     | 4.31     | 0.17      | 0.17      | 3.12     | 5.96      | 8.84      | 9.94E-19 |
| Maximally adjusted | Women | 3-4   | 2.51     | 0.17      | 0.17      | 1.82     | 3.47      | 5.58      | 2.46E-08 |
| Maximally adjusted | Women | 5-8   | 1.67     | 0.17      | 0.17      | 1.20     | 2.32      | 3.05      | 2.32E-03 |
| Maximally adjusted | Women | 9-12  | 1.58     | 0.20      | 0.20      | 1.08     | 2.33      | 2.34      | 1.94E-02 |
| Maximally adjusted | Women | 13-26 | 1.66     | 0.11      | 0.12      | 1.32     | 2.08      | 4.39      | 1.11E-05 |
| Maximally adjusted | Women | 27-49 | 1.16     | 0.22      | 0.22      | 0.75     | 1.81      | 0.67      | 5.01E-01 |
