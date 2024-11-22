examples = [
    {
        "input": "Return all variants that are associated with Non-small_cell_lung_carcinoma with \"drug_response\" clinical significance",
        "query": """
SELECT
    concat('chr', c.contigname) as contigname,
    c.start,
    c.referenceallele,
    c.alternatealleles,
    c.attributes['GENEINFO'] as gene_info,
    c.attributes['CLNSIG'] as clinical_significance,
    c.attributes['CLNDN'] as disease_name,
    c.sampleid,
    g."names",
    g.attributes,
    g.contigname as contigname_gnomad,
    g."start",
    g.sampleid
from omicsdb.clinvar c
LEFT JOIN omicsdb.gnomad g on c."end" = g."end" AND g.contigname = concat('chr', c.contigname)
where 1=1
    and c.attributes['CLNDN'] like '%Non-small_cell_lung_carcinoma%'
    and c.attributes['CLNSIG'] in ('drug_response')
"""
        },{
        "input": "Return all variants that are associated with `Tyrosine_kinase_inhibitor_response` with `Pathogenic/Likely_pathogenic` clinical significance",
        "query": """
SELECT
    concat('chr', c.contigname) as contigname,
    c.start,
    c.referenceallele,
    c.alternatealleles,
    c.attributes['GENEINFO'] as gene_info,
    c.attributes['CLNSIG'] as clinical_significance,
    c.attributes['CLNDN'] as disease_name,
    c.sampleid,
    g."names",
    g.attributes,
    g.contigname as contigname_gnomad,
    g."start",
    g.sampleid
from omicsdb.clinvar c
LEFT JOIN omicsdb.gnomad g on c."end" = g."end" AND g.contigname = concat('chr', c.contigname)
where 1=1
    and c.attributes['CLNDN'] like '%Tyrosine_kinase_inhibitor_response%'
    and c.attributes['CLNSIG'] in ('Pathogenic/Likely_pathogenic')
""",
        },
]
