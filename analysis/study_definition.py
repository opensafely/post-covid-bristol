from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv,
)  # NOQA
from variable_loop import get_codelist_variable

placeholder_ctv3 = codelist(["codes"], system="ctv3")
placeholder_icd10 = codelist(["codes"], system="icd10")
placeholder_dmd = codelist(["codes"], system="snomed")

variables = {
    "cov_ever_ami": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_pe_vt": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_icvt": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_all_stroke": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_thrombophilia": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_tcp": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_dementia": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_liver_disease": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_ckd": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_cancer": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_diabetes": [placeholder_ctv3, placeholder_icd10, placeholder_dmd],
    "cov_ever_obesity": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_depression": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_copd": [placeholder_ctv3, placeholder_icd10],
    "cov_antiplatelet_meds": [placeholder_dmd],
    "cov_lipid_meds": [placeholder_dmd],
    "cov_anticoagulation_meds": [placeholder_dmd],
    "cov_cocp_meds": [placeholder_dmd],
    "cov_hrt_meds": [placeholder_dmd],
    "cov_ever_other_arterial_embolism": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_dic": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_mesenteric_thrombus": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_artery_dissect": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_life_arrhythmia": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_cardiomyopathy": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_hf": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_pericarditis": [placeholder_ctv3, placeholder_icd10],
    "cov_ever_myocarditis": [placeholder_ctv3, placeholder_icd10],
}

covariates = {k: get_codelist_variable(v) for k, v in variables.items()}


study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),
    index_date="2020-02-01",
    **covariates,
)
