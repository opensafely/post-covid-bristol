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

def generate_deprivation_ntile_dictionary(ntiles:int) -> dict:
    dep_dict={"0": "DEFAULT"}
    for n in range(1,ntiles+1):
        l = f"index_of_multiple_deprivation >={1 if n==1 else f'32844*{n-1}/{ntiles}'}"
        r = f" AND index_of_multiple_deprivation < 32844*{n}/{ntiles}"

        dep_dict[str(n)] = l if n==ntiles else l+r

    return dep_dict

def generate_universal_expectations(n_categories:int) -> dict:
    equal_ratio = round(1/n_categories,2)
    ratios = {str(n):equal_ratio for n in range(1,n_categories)}
    ratios["0"]= 0.01
    ratios[str(n_categories)] = 1-sum(ratios.values())

    exp_dict = {"rate": "universal",
                "category": {"ratios":ratios}
                }

    return exp_dict

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
            use_most_frequent_code=True
        ),

        cov_ethnicity_gp_opensafely=patients.with_these_clinical_events(
            codelists.opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True
        ),
        
        cov_ethnicity_gp_primis=patients.with_these_clinical_events(
            codelists.primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True
        ),

        cov_ethnicity_gp_opensafely_date=patients.with_these_clinical_events(
            codelists.opensafely_ethnicity_codes_16,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True
        ),
        
        cov_ethnicity_gp_primis_date=patients.with_these_clinical_events(
            codelists.primis_covid19_vacc_update_ethnicity,
            on_or_before="index_date",
            returning="category",
            find_last_match_in_period=True
        ),
        return_expectations=generate_universal_expectations(16)
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
    ),

    cov_deprivation=patients.categorised_as(
        generate_deprivation_ntile_dictionary(10),
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0" : 0.01,
                    "1" : 0.1,
                    "2" : 0.1,
                    "3" : 0.1,
                    "4" : 0.1,
                    "5" : 0.1,
                    "6" : 0.1,
                    "7" : 0.1,
                    "8" : 0.1,
                    "9" : 0.1,
                    "10": 0.09,
                }
            },
        },
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
    )
)
