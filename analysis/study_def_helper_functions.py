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