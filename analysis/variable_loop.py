from cohortextractor import patients
import inspect
import random


def get_variable_definition(codelist):
    if codelist.system == "ctv3":
        return patients.with_these_clinical_events(codelist, on_or_after="index_date")
    if codelist.system == "icd10":
        return patients.admitted_to_hospital(
            with_these_diagnoses=codelist, on_or_before="index_date"
        )
    if codelist.system == "snomed":
        return patients.with_these_medications(codelist, on_or_before="index_date")


def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [
            var_name
            for var_name, var_val in fi.frame.f_locals.items()
            if var_val is var
        ]
        if len(names) > 0:
            return names[0] + str(random.randint(1, 1000))


def get_codelist_variable(codelists):
    if len(codelists) > 1:
        string_list = [retrieve_name(v) for v in codelists]
        logic = " OR ".join(string_list)
        sub_var_dict = {
            f"{s}": get_variable_definition(c) for s, c in zip(string_list, codelists)
        }
        return patients.satisfying(logic, **sub_var_dict)
    else:
        return get_variable_definition(codelists[0])
