from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    filter_codes_by_category,
)
import codelists
import study_def_helper_functions as helpers
from variable_loop import get_codelist_variable

placeholder_ctv3 = codelist(["codes"], system="ctv3")
placeholder_icd10 = codelist(["codes"], system="icd10")
placeholder_dmd = codelist(["codes"], system="snomed")

variables = {
    "cov_ever_ami": [ami_snomed, ami_icd10, ami_prior_icd10],
    "cov_ever_pe_vt": [pe_icd10, pe_snomed, dvt_dvt_icd10, other_dvt_icd10, dvt_pregnancy_icd10, icvt_pregnancy_icd10, portal_vein_thrombosis_icd10, vt_icd10],
    "cov_ever_icvt": [dvt_icvt_icd10, dvt_icvt_snomed],
    "cov_ever_all_stroke": [stroke_isch_icd10, stroke_isch_snomed, stroke_sah_hs_icd10, stroke_sah_hs_snomed],
    "cov_ever_thrombophilia": [thrombophilia_snomed, thrombophilia_icd10],
    "cov_ever_tcp": [thrombocytopenia_icd10, ttp_icd10, tcp_snomed],
    "cov_ever_dementia": [dementia_snomed, dementia_icd10, dementia_vascular_snomed, dementia_vascular_icd10],
    "cov_ever_liver_disease": [liver_disease_snomed, liver_disease_icd10],
    "cov_ever_ckd": [ckd_snomed, ckd_icd10],
    "cov_ever_cancer": [cancer_snomed, cancer_icd10],
    "cov_ever_hypertension": [hypertension_icd10, hypertension_drugs, hypertension_snomed],
    "cov_ever_diabetes": [diabetes_snomed, diabetes_icd10, diabetes_drugs],
    "cov_ever_obesity": [bmi_obesity_snomed, bmi_obesity_icd10],
    "cov_ever_depression": [depression_snomed, depression_icd10],
    "cov_ever_copd": [copd_snomed, copd_icd10],
    "cov_antiplatelet_meds": [antiplatelet],
    "cov_lipid_meds": [lipid_lowering],
    "cov_anticoagulation_meds": [anticoagulant],
    "cov_cocp_meds": [cocp],
    "cov_hrt_meds": [hrt],
    "cov_ever_other_arterial_embolism": [other_arterial_embolism_icd10],
    "cov_ever_dic": [dic_icd10],
    "cov_ever_mesenteric_thrombus": [mesenteric_thrombus_icd10],
    "cov_ever_artery_dissect": [artery_dissect_icd10],
    "cov_ever_life_arrhythmia": [life_arrhythmia_icd10],
    "cov_ever_cardiomyopathy": [cardiomyopathy_snomed, cardiomyopathy_icd10],
    "cov_ever_hf": [hf_snomed, hf_icd10],
    "cov_ever_pericarditis": [pericarditis_icd10],
    "cov_ever_myocarditis": [myocarditis_icd10],
}

covariates = {k: get_codelist_variable(v) for k, v in variables.items()}

study = StudyDefinition(
    # placeholder index date
    index_date="2001-01-01",
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),
    ###
    # Used to support combined death_date variable.
    # Ideally would be contained within minimum_of()
    primary_care_death_date=patients.with_death_recorded_in_primary_care(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "index_date"},
            "rate": "exponential_increase",
        },
    ),
    ons_died_from_any_cause_date=patients.died_from_any_cause(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "index_date"},
            "rate": "exponential_increase",
        },
    ),
    ###
    death_date=patients.minimum_of(
        "primary_care_death_date", "ons_died_from_any_cause_date"
    ),
    cov_sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    cov_age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    cov_ethnicity=patients.categorised_as(
        helpers.generate_ethnicity_dictionary(16),
        cov_ethnicity_sus=patients.with_ethnicity_from_sus(
            returning="group_16", use_most_frequent_code=True
        ),
        cov_ethnicity_gp_opensafely=patients.with_these_clinical_events(
            codelists.opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_primis=patients.with_these_clinical_events(
            codelists.primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_opensafely_date=patients.with_these_clinical_events(
            codelists.opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_primis_date=patients.with_these_clinical_events(
            codelists.primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        return_expectations=helpers.generate_universal_expectations(16),
    ),
    cov_smoking_status=patients.categorised_as(
        {
            "S": "most_recent_smoking_code = 'S'",
            "E": """
                 most_recent_smoking_code = 'E' OR (
                   most_recent_smoking_code = 'N' AND ever_smoked
                 )
            """,
            "N": "most_recent_smoking_code = 'N' AND NOT ever_smoked",
            "M": "DEFAULT",
        },
        return_expectations={
            "category": {"ratios": {"S": 0.6, "E": 0.1, "N": 0.2, "M": 0.1}}
        },
        most_recent_smoking_code=patients.with_these_clinical_events(
            codelists.smoking_clear,
            find_last_match_in_period=True,
            on_or_before="index_date",
            returning="category",
        ),
        ever_smoked=patients.with_these_clinical_events(
            filter_codes_by_category(codelists.smoking_clear, include=["S", "E"]),
            on_or_before="index_date",
        ),
    ),
    cov_deprivation=patients.categorised_as(
        helpers.generate_deprivation_ntile_dictionary(10),
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations=helpers.generate_universal_expectations(10),
    ),
    cov_region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.2,
                    "South East": 0.2,
                },
            },
        },
    ),
    cov_ever_ami=patients.with_these_clinical_events(
        codelist, # how do I define codelists making use of get_codelist_variable (line 47)
        return_expectations=None, # enter the expected proportion of patients with ever AMI here?
        on_or_before="index_date", 
        returning='binary_flag', 
        ),
    **covariates,
)
