from cohortextractor import StudyDefinition, patients
import codelists


def generate_ethnicity_dictionary(n_groups:int) -> dict:
    eth_dict={"0":"DEFAULT"}
    for n in range(1,n_groups+1):
        eth_dict[str(n)] = f""" 
            (cov_ethnicity_sus="{n}" AND cov_ethnicity_gp_opensafely="" AND cov_ethnicity_gp_primis="") OR
            (cov_ethnicity_gp_opensafely="{n}" AND cov_ethnicity_gp_opensafely_date >= cov_ethnicity_gp_primis_date ) OR
            (cov_ethnicity_gp_primis="{n}" AND cov_ethnicity_gp_primis_date > cov_ethnicity_gp_opensafely_date)            
            """
    return eth_dict


study = StudyDefinition(
    #placeholder index date
    index_date="2001-01-01",

    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },

    population=patients.all(),

    ###
    # Used to support combined death_date variable. 
    # Ideally would be contained within minimum_of()
    primary_care_death_date=patients.with_death_recorded_in_primary_care(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest" : "index_date"},
            "rate" : "exponential_increase"
        }
    ),
    cpns_death_date=patients.with_death_recorded_in_cpns(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest" : "index_date"},
            "rate" : "exponential_increase"
        }
    ),
    ons_died_from_any_cause_date=patients.died_from_any_cause(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest" : "index_date"},
            "rate" : "exponential_increase"
        }
    ),
    ###

    death_date=patients.minimum_of("primary_care_death_date","cpns_death_date","ons_died_from_any_cause_date"),

    cov_sex=patients.sex(
    return_expectations={
        "rate": "universal",
        "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),

    cov_age=patients.age_as_of(
    "index_date",
    return_expectations={
        "rate" : "universal",
        "int" : {"distribution" : "population_ages"}
        }
    ),

    cov_ethnicity=patients.categorised_as(generate_ethnicity_dictionary(16),

        cov_ethnicity_sus=patients.with_ethnicity_from_sus(
            returning="group_16",
            use_most_frequent_code=True,
            return_expectations={
                "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                "incidence": 0.75,
            }
        ),

        cov_ethnicity_gp_opensafely=patients.with_these_clinical_events(
            codelists.opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
            return_expectations={
                "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                "incidence": 0.75,
            }
        ),
        
        cov_ethnicity_gp_primis=patients.with_these_clinical_events(
            codelists.primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
            return_expectations={
                "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                "incidence": 0.75,
            }
        ),

        cov_ethnicity_gp_opensafely_date=patients.with_these_clinical_events(
            codelists.opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
            return_expectations={
                "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                "incidence": 0.75,
            }
        ),
        
        cov_ethnicity_gp_primis_date=patients.with_these_clinical_events(
            codelists.primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True,
            return_expectations={
                "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
                "incidence": 0.75,
            }
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.01,
                    "1": 0.20,
                    "2": 0.20,
                    "3": 0.20,
                    "4": 0.20,
                    "5": 0.19
                }
            },
        },
    ),

    cov_smoking_status_clear = patients.with_these_clinical_events(
        codelists.smoking_clear,
        on_or_before="index_date",
        find_last_match_in_period=True,
        return_expectations={
            "incidence":0.7,
            "category":{
                "ratios": {
                    "S":0.1,
                    "N":0.7,
                    "E":0.2
                }
            }
        }
    ),

    cov_smoking_status_unclear = patients.with_these_clinical_events(
        codelists.smoking_unclear,
        on_or_before="index_date",
        find_last_match_in_period=True,
        return_expectations={
            "incidence":0.7,
            "category":{
                "ratios": {
                    "S":0.1,
                    "N":0.7,
                    "E":0.2
                }
            }
        }
    )
)
