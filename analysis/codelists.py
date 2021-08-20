from os import system
from cohortextractor import codelist, codelist_from_csv

opensafely_ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_16",
)

primis_covid19_vacc_update_ethnicity = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth2001.csv",
    system="snomed",
    column="code",
    category_column="grouping_16_id",
)

smoking_clear = codelist_from_csv(
    "codelists/opensafely-smoking-clear.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="Category",
)

smoking_unclear = codelist_from_csv(
    "codelists/opensafely-smoking-unclear.csv",
    system="ctv3",
    column="CTV3Code",
    category_column="Category",
)

ami_snomed = codelist_from_csv(
    "user/elsie_horne/ami_snomed/36d11028.csv",
    system="snomed",
    column="code",
)

ami_icd10 = codelist_from_csv(
    "user/elsie_horne/ami_snomed/4f19cfce.csv",
    system="icd10",
    column="code",
)

ami_prior_icd10 = codelist_from_csv(
    "user/elsie_horne/ami_prior_icd10/360a5c99.csv",
    system="icd10",
    column="code",
)

artery_dissect_icd10 = codelist_from_csv(
    "user/elsie_horne/artery_dissect_icd10/20745ce9.csv",
    system="icd10",
    column="code",
)

bmi_obesity_snomed = codelist_from_csv(
    "user/elsie_horne/bmi_obesity_snomed/0764e9b4.csv",
    system="snomed",
    column="code",
)

bmi_obesity_icd10 = codelist_from_csv(
    "user/elsie_horne/bmi_obesity_icd10/6e55767e.csv",
    system="icd10",
    column="code",
)

cancer_snomed = codelist_from_csv(
    "user/elsie_horne/cancer_snomed/23271cdf.csv",
    system="snomed",
    column="code",
)

cancer_icd10 = codelist_from_csv(
    "user/elsie_horne/cancer_icd10/55460349.csv",
    system="icd10",
    column="code",
)
cardiomyopathy_snomed = codelist_from_csv(
    "user/elsie_horne/cardiomyopathy_snomed/0a17a9aa.csv",
    system="snomed",
    column="code",
)

cardiomyopathy_icd10 = codelist_from_csv(
    "user/elsie_horne/cardiomyopathy_icd10/71083674.csv",
    system="icd10",
    column="code",
)

ckd_snomed = codelist_from_csv(
    "user/elsie_horne/ckd_snomed/25d9dcd5.csv",
    system="snomed",
    column="code",
)

ckd_icd10 = codelist_from_csv(
    "user/elsie_horne/ckd_icd10/0cca69a0.csv",
    system="icd10",
    column="code",
)

copd_snomed = codelist_from_csv(
    "user/elsie_horne/copd_snomed/419c1000.csv",
    system="snomed",
    column="code",
)

copd_icd10 = codelist_from_csv(
    "user/elsie_horne/copd_icd10/5aab8335.csv",
    system="icd10",
    column="code",
)

dementia_snomed = codelist_from_csv(
    "user/elsie_horne/dementia_snomed/7bd3364ccsv",
    system="snomed",
    column="code",
)

dementia_icd10 = codelist_from_csv(
    "user/elsie_horne/dementia_icd10/2df21cb7.csv",
    system="icd10",
    column="code",
)

dic_icd10 = codelist_from_csv(
    "user/elsie_horne/dic_icd10/62c3c317.csv",
    system="icd10",
    column="code",
)

dvt_dvt_icd10 = codelist_from_csv(
    "user/elsie_horne/dvt_dvt_icd10/49b44fe2.csv",
    system="icd10",
    column="code",
)

dvt_icvt_icd10 = codelist_from_csv(
    "user/elsie_horne/dvt_icvt_icd10/30a4dcad.csv",
    system="icd10",
    column="code",
)

dvt_icvt_snomed = codelist_from_csv(
    "user/elsie_horne/dvt_icvt_snomed/7e85f642.csv",
    system="snomed",
    column="code",
)

dvt_pregnancy_icd10 = codelist_from_csv(
    "user/elsie_horne/dvt_pregnancy_icd10/6576830d.csv",
    system="icd10",
    column="code",
)

hf_snomed = codelist_from_csv(
    "user/elsie_horne/hf_snomed/33579ca3.csv",
    system="snomed",
    column="code",
)

hf_icd10 = codelist_from_csv(
    "user/elsie_horne/hf_icd10/4c670fd8.csv",
    system="icd10",
    column="code",
)

stroke_isch_icd10 = codelist_from_csv(
    "user/elsie_horne/stroke_isch_icd10/03eb762f.csv",
    system="icd10",
    column="code",
)

stroke_isch_snomed = codelist_from_csv(
    "user/elsie_horne/stroke_isch_snomed/1cfae964.csv",
    system="snomed",
    column="code",
)

stroke_sah_hs_icd10 = codelist_from_csv(
    "user/elsie_horne/stroke_sah_hs_icd10/51cc8fc4.csv",
    system="icd10",
    column="code",
)

stroke_sah_hs_snomed = codelist_from_csv(
    "user/elsie_horne/stroke_sah_hs_snomed/6adc02f9.csv",
    system="snomed",
    column="code",
)

pe_icd10 = codelist_from_csv(
    "user/elsie_horne/pe_icd10/069e3625.csv",
    system="icd10",
    column="code",
)

pe_snomed = codelist_from_csv(
    "user/elsie_horne/pe_snomed/6d8ec2ef.csv",
    system="snomed",
    column="code",
)

other_dvt_icd10 = codelist_from_csv(
    "user/elsie_horne/other_dvt_icd10/547f4fba.csv",
    system="icd10",
    column="code",
)

icvt_pregnancy_icd10 = codelist_from_csv(
    "user/elsie_horne/icvt_pregnancy_icd10/3b6fdc85.csv",
    system="icd10",
    column="code",
)

portal_vein_thrombosis_icd10 = codelist_from_csv(
    "user/elsie_horne/portal_vein_thrombosis_icd10/22606950.csv",
    system="icd10",
    column="code",
)

vt_icd10 = codelist_from_csv(
    "user/elsie_horne/vt_icd10/0950f61b.csv",
    system="icd10",
    column="code",
)

thrombophilia_icd10 = codelist_from_csv(
    "user/elsie_horne/thrombophilia_icd10/704182e5.csv",
    system="icd10",
    column="code",
)

thrombophilia_snomed = codelist_from_csv(
    "user/elsie_horne/thrombophilia_snomed/57320fb0.csv",
    system="snomed",
    column="code",
)

tcp_snomed = codelist_from_csv(
    "user/elsie_horne/tcp_snomed/3e229c7b.csv",
    system="snomed",
    column="code",
)

ttp_icd10 = codelist_from_csv(
    "user/elsie_horne/ttp_icd10/25132946.csv",
    system="icd10",
    column="code",
)

thrombocytopenia_icd10 = codelist_from_csv(
    "user/elsie_horne/thrombocytopenia_icd10/0c03b611.csv",
    system="icd10",
    column="code",
)

dementia_vascular_snomed = codelist_from_csv(
    "user/elsie_horne/dementia_vascular_snomed/0eb67607.csv",
    system="snomed",
    column="code",
)

dementia_vascular_icd10 = codelist_from_csv(
    "user/elsie_horne/dementia_vascular_icd10/27c5e93c.csv",
    system="icd10",
    column="code",
)

liver_disease_snomed = codelist_from_csv(
    "user/elsie_horne/liver_disease_snomed/5c978f9c.csv",
    system="snomed",
    column="code",
)

liver_disease_icd10 = codelist_from_csv(
    "user/elsie_horne/liver_disease_icd10/75a702d1.csv",
    system="icd10",
    column="code",
)

diabetes_snomed = codelist_from_csv(
    "user/elsie_horne/diabetes_snomed/43881c67.csv",
    system="snomed",
    column="code",
)

diabetes_icd10 = codelist_from_csv(
    "user/elsie_horne/diabetes_icd10/2a78a932.csv",
    system="icd10",
    column="code",
)

diabetes_drugs = codelist_from_csv(
    "opensafely/bristol_diabetes_drugs/60110321.csv",
    system="snomed",
    column="code",
)

depression_icd10 = codelist_from_csv(
    "user/elsie_horne/depression_icd10/116935fd.csv",
    system="icd10",
    column="code",
)

depression_snomed = codelist_from_csv(
    "user/elsie_horne/depression_snomed/7859c2c7.csv",
    system="snomed",
    column="code",
)

antiplatelet = codelist_from_csv(
    "user/elsie_horne/antiplatelet/316b903c.csv",
    system="snomed",
    column="code",
)

lipid_lowering = codelist_from_csv(
    "user/elsie_horne/lipid_lowering/341e5032.csv",
    system="snomed",
    column="code",
)

anticoagulant = codelist_from_csv(
    "user/elsie_horne/anticoagulant/4a7b0371.csv",
    system="snomed",
    column="code",
)

cocp = codelist_from_csv(
    "user/elsie_horne/cocp/185c1d07.csv",
    system="snomed",
    column="code",
)

hrt = codelist_from_csv(
    "user/elsie_horne/hrt/7f4ca9d1.csv",
    system="snomed",
    column="code",
)

other_arterial_embolism_icd10 = codelist_from_csv(
    "user/elsie_horne/other_arterial_embolism_icd10/463adc5d.csv",
    system="icd10",
    column="code",
)

mesenteric_thrombus_icd10 = codelist_from_csv(
    "user/elsie_horne/mesenteric_thrombus_icd10/2d2b6928.csv",
    system="icd10",
    column="code",
)

life_arrhythmia_icd10 = codelist_from_csv(
    "user/elsie_horne/life_arrhythmia_icd10/141bf5f3.csv",
    system="icd10",
    column="code",
)

pericarditis_icd10 = codelist_from_csv(
    "user/elsie_horne/pericarditis_icd10/7b0c82bd.csv",
    system="icd10",
    column="code",
)

myocarditis_icd10 = codelist_from_csv(
    "user/elsie_horne/myocarditis_icd10/48ed9c53.csv",
    system="icd10",
    column="code",
)

hypertension_icd10 = codelist_from_csv(
    "user/elsie_horne/hypertension_icd10/1a48296e.csv",
    system="icd10",
    column="code",
)

hypertension_drugs = codelist_from_csv(
    "opensafely/bristol_hypertension/79207656.csv",
    system="snomed",
    column="code",
)

hypertension_snomed = codelist_from_csv(
    "nhsd-primary-care-domain-refsets/hyp_cod/20210127.csv",
    system="snomed",
    column="code",
)