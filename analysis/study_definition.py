from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    filter_codes_by_category,
    combine_codelists,
)
from codelists import *
import study_def_helper_functions as helpers
from variable_loop import get_codelist_variable

placeholder_ctv3 = codelist(["codes"], system="ctv3")
placeholder_snomed_clinical = codelist(["codes"], system="snomed")
placeholder_icd10 = codelist(["codes"], system="icd10")
placeholder_dmd = codelist(["dmd_id"], system="snomed")

variables = {
    "cov_ever_ami": [ami_snomed_clinical, ami_icd10, ami_prior_icd10],
    "cov_ever_pe_vt": [pe_icd10, pe_snomed_clinical, dvt_dvt_icd10, other_dvt_icd10, dvt_pregnancy_icd10, icvt_pregnancy_icd10, portal_vein_thrombosis_icd10, vt_icd10],
    "cov_ever_icvt": [dvt_icvt_icd10, dvt_icvt_snomed_clinical],
    "cov_ever_all_stroke": [stroke_isch_icd10, stroke_isch_snomed_clinical, stroke_sah_hs_icd10, stroke_sah_hs_snomed_clinical],
    "cov_ever_thrombophilia": [thrombophilia_snomed_clinical, thrombophilia_icd10],
    "cov_ever_tcp": [thrombocytopenia_icd10, ttp_icd10, tcp_snomed_clinical],
    "cov_ever_dementia": [dementia_snomed_clinical, dementia_icd10, dementia_vascular_snomed_clinical, dementia_vascular_icd10],
    "cov_ever_liver_disease": [liver_disease_snomed_clinical, liver_disease_icd10],
    "cov_ever_ckd": [ckd_snomed_clinical, ckd_icd10],
    "cov_ever_cancer": [cancer_snomed_clinical, cancer_icd10],
    "cov_ever_hypertension": [hypertension_icd10, hypertension_drugs_dmd, hypertension_snomed_clinical],
    "cov_ever_diabetes": [diabetes_snomed_clinical, diabetes_icd10, diabetes_drugs_dmd],
    "cov_ever_obesity": [bmi_obesity_snomed_clinical, bmi_obesity_icd10],
    "cov_ever_depression": [depression_snomed_clinical, depression_icd10],
    "cov_ever_copd": [copd_snomed_clinical, copd_icd10],
    "cov_antiplatelet_meds": [antiplatelet_dmd],
    "cov_lipid_meds": [lipid_lowering_dmd],
    "cov_anticoagulation_meds": [anticoagulant_dmd],
    "cov_cocp_meds": [cocp_dmd],
    "cov_hrt_meds": [hrt_dmd],
    "cov_ever_other_arterial_embolism": [other_arterial_embolism_icd10],
    "cov_ever_dic": [dic_icd10],
    "cov_ever_mesenteric_thrombus": [mesenteric_thrombus_icd10],
    "cov_ever_artery_dissect": [artery_dissect_icd10],
    "cov_ever_life_arrhythmia": [life_arrhythmia_icd10],
    "cov_ever_cardiomyopathy": [cardiomyopathy_snomed_clinical, cardiomyopathy_icd10],
    "cov_ever_hf": [hf_snomed_clinical, hf_icd10],
    "cov_ever_pericarditis": [pericarditis_icd10],
    "cov_ever_myocarditis": [myocarditis_icd10],

}

covariates = {k: get_codelist_variable(v) for k, v in variables.items()}

study = StudyDefinition(
    # Placeholder index date
    index_date="2020-01-01",
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    # Require practice registration for a year prior to index date
    population=patients.registered_with_one_practice_between(
        "index_date - 1 year", "index_date"
    ),
    # Record death date
    primary_care_death_date=patients.with_death_recorded_in_primary_care(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "exponential_increase",
        },
    ),
    ons_died_from_any_cause_date=patients.died_from_any_cause(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "exponential_increase",
        },
    ),
    death_date=patients.minimum_of(
        "primary_care_death_date", "ons_died_from_any_cause_date"
    ),
    # Record COVID-19 infection date
    sgss_covid19_date=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        on_or_after="index_date",
        return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.05,
        },
    ),
    primary_care_covid19_date=patients.with_these_clinical_events(
        combine_codelists(
            covid_primary_care_code,
            covid_primary_care_positive_test,
            covid_primary_care_sequalae,
        ),
        returning="date",
        on_or_after="index_date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.05,
        },
    ),
    hospital_covid19_date=patients.admitted_to_hospital(
        with_these_diagnoses=covid_codes,
        returning="date_admitted",
        on_or_after="index_date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.05,
        },
    ),
    death_covid19_date=patients.with_these_codes_on_death_certificate(
        covid_codes,
        returning="date_of_death",
        on_or_after="index_date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.02
        },
    ),
    exp_confirmed_covid19_date=patients.minimum_of(
        "sgss_covid19_date","primary_care_covid19_date","hospital_covid19_date","death_covid19_date"
    ),
    # First covid vaccination date (first vaccine given on 8/12/2020 in the UK)
    covid19_vaccination_date1=patients.with_tpp_vaccination_record(
        # code for TPP only, when using patients.with_tpp_vaccination_record() function
        target_disease_matches="SARS-2 CORONAVIRUS",
        on_or_after="2020-12-07",
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "2020-12-08", "latest": "today"},
            "incidence": 0.7
        },
    ),
    # Second covid vaccination date (first second dose reported on 29/12/2020 in the UK)
    covid19_vaccination_date2=patients.with_tpp_vaccination_record(
        # code for TPP only, when using patients.with_tpp_vaccination_record() function
        target_disease_matches="SARS-2 CORONAVIRUS",
        on_or_after="covid19_vaccination_date1 + 14 days",  # Allowing for less days between 2 vaccination dates
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest": "2020-12-29", "latest": "today"},
            "incidence": 0.6
        },
    ),
    # Record acute myocardial infarction date
    ami_snomed=patients.with_these_clinical_events(
        ami_snomed_clinical,
        returning="date",
        on_or_after="index_date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
         return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.03,
        },
    ),
    ami_icd10=patients.admitted_to_hospital(
        returning="date_admitted",
        with_these_diagnoses=ami_icd10,
        on_or_after="index_date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
         return_expectations={
            "date": {"earliest": "index_date", "latest" : "today"},
            "rate": "uniform",
            "incidence": 0.03,
        },
    ),
    out_AMI=patients.minimum_of(
        "ami_snomed", "ami_icd10"
    ),
    # Covariates
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
            opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_primis=patients.with_these_clinical_events(
            primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_opensafely_date=patients.with_these_clinical_events(
            opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
        ),
        cov_ethnicity_gp_primis_date=patients.with_these_clinical_events(
            primis_covid19_vacc_update_ethnicity,
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
            smoking_clear,
            find_last_match_in_period=True,
            on_or_before="index_date",
            returning="category",
        ),
        ever_smoked=patients.with_these_clinical_events(
            filter_codes_by_category(smoking_clear, include=["S", "E"]),
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
    cov_n_disorder=patients.with_gp_consultations(
        between=["index_date - 12 months", "index_date"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 10, "stddev": 3},
            "incidence": 1,
        },
    ),
    **covariates,
)
