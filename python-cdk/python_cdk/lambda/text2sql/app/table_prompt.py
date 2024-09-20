genomad_prompt = """
    <table>
        <table_name>
        genomad
        </table_name>

        <table_description>
        The Genome Aggregation Database (gnomAD), originally launched in 2014 as the Exome Aggregation Consortium
        (ExAC), is the result of a coalition of investigators willing to share aggregate exome and genome sequencing 
        data from a variety of large-scale sequencing projects, and make summary data available for the wider 
        scientific community. The gnomAD database is composed of exome and genome sequences from around the world. 
                
        This table contains information about genes. Each row has columns to identify a gene. Use the following columns
        to identify a variant: `contigname`, `start`, `end`, `referenceallele`, `alternatealleles`. These columns refer
        to a chromosome number (`contigname`), a start position (`start`), and an end position (`end`), the 
        reference allele of the variant, and the alternate alleles. If the question mentions a
        particular gene, this is probably the table to use.  This table should be used to map from a gene to all
        variants associated with that gene. 
        
        If the question want to know about a particular gene given a gene name, for example: "What is the allele
        frequency of gene `rs121434569` or `{RS121434569}`?", then you should use the column names. Remember to
        use the following syntax to extract each individual name from the `names` array column. The syntax is
        `select * from omicsdb.genomad cross join unnest(names) as t(name) where name in ('rs121434569', 'RS121434569').
`
        </table_description>

        <column>
            <column_name>contigname</column_name>
            <column_description>
                The chromossome where the variant is located. It is prefixed by the string "chr" and a number between 1 and 22.
            </column_description>
            <example_use>
              SELECT * FROM genomad WHERE contigname = 'chr7';
            </example_use>
        </column>
        <column>
            <column_name>start</column_name>
            <column_description>
                The start position of the variant on the chromosome. This should be used to compose the primary key of the variant,
                along with the following tables: `contigname`, `end`, `referenceallele`, `alternatealleles`.
            </column_description>
            <example_use>
              SELECT * FROM genomad WHERE start > 100000 and end < 200000;
            </example_use>
        </column>
        <column>
            <column_name>end</column_name>
            <column_description>
                The end position of the variant on the chromosome. This should be used to compose the primary key of the variant,
                along with the following tables: `contigname`, `start`, `referenceallele`, `alternatealleles`.
            </column_description>
            <example_use>
              SELECT * FROM genomad WHERE and start > 100000 and end < 200000;
            </example_use>
        </column>
        <column>
            <column_name>names</column_name>
            <column_description>
                A semi-colon separated list of unique identifiers for the variant. This often includes dbSNP IDs (e.g., rsIDs).
            </column_description>
            <example_use>
                select * from genomad
                cross join unnest(names) as t(name)
                where name in ('rs112353164','rs1218977723')
            </example_use>
        </column>
        <column>
            <column_name>referenceallele</column_name>
            <column_description>The reference allele of the variant</column_description>
            <example_use>
              SELECT * FROM genomad WHERE referenceallele = 'XXXXXXXXXXXXXXX';
            </example_use>
        </column>
        <column>
            <column_name>alternatealleles</column_name>
            <column_description>An array of alternate alleles for the variant</column_description>
            <example_use>
                SELECT * FROM genomad
                cross join unnest(alternatealleles) as t(alternateallele)
                where alternateallele in ('G', 'T')
                limit 100;
            </example_use>
        </column>
        
        <column>
            <column_name>filters</column_name>
            <column_description>
                The filter status of a variant in the gnomAD dataset indicates whether the variant has passed quality 
                control filters. Variants that do not pass certain thresholds for quality metrics are flagged with 
                specific filter labels. Here are some common filter statuses you might encounter in gnomAD data:

                `PASS`: The variant has passed all quality control filters.
                `RF`: Random Forest filter indicating that the variant did not meet the thresholds set by a random forest classifier used to distinguish true variants from sequencing artifacts.
                `AC0`: Allele Count 0 filter indicating that the variant has zero allele counts after filtering out low confidence genotypes.
                `InbreedingCoeff`: Inbreeding Coefficient filter indicating that the variant has an inbreeding coefficient less than -0.3, suggesting possible genotyping errors.
                `AS_VQSR`: Allele-Specific Variant Quality Score Recalibration filter is a filter status applied to variants based on a statistical model that recalibrates the variant quality scores. This process involves constructing a model that differentiates between true variants and sequencing artifacts using known variant sites and a set of quality metrics. 
            
                These filters help ensure the reliability of the data used for downstream analyses.
            </column_description>
            <example_use>
                select * from genomad
                    cross join unnest(filters) as t(filter)
                WHERE filter NOT LIKE '%AC0%'
                AND start between 128401319 and 129401319;
            </example_use>
        </column>
        <column>
            <column_name>splitfrommultiallelic</column_name>
            <column_description>
                Multi-allelic Sites: These are genomic positions where more than one type of mutation (alternate allele) occurs. For example, at a given position, the reference allele might be A, and the alternate alleles might be T and G.
                Splitting Process: During the variant calling process, tools like GATK can split multi-allelic sites into multiple bi-allelic records. This means that instead of having a single record with multiple alternate alleles, there will be multiple records each with one alternate allele.
                Purpose of `splitfrommultiallelic`: This field indicates whether a variant record was created as a result of this splitting process. It helps users understand that the variant was originally part of a more complex multi-allelic site.
            </column_description>
            <example_use>
                select * from genomad
                where splitfrommultiallelic = false
                AND start between 129401219 and 129401329;
            </example_use>
        </column>
        <column>
            <column_name>attributes</column_name>
            <column_description>
                The attributes column in the gnomAD data typically contains a variety of annotations and metadata about each genetic
                variant. These attributes provide detailed information on the variant's properties, including its functional impact,
                frequency in different populations, quality metrics, and other relevant data points. Below is an explanation of some
                common attributes you might find in this column. The attributes in GenomAD data are:
                
                `AC`: Allele Count. Definition: The number of times the alternate allele is observed in the dataset. Purpose: Provides 
                insight into how common a variant is in the population.
                
                `AF`: Allele Frequency. Definition: The frequency of the alternate allele in the dataset. Purpose: Indicates how 
                common or rare a variant is in the population. 
            </column_description>
            <example_use>
                select * from genomad
                where TRY_CAST(attributes['AF'] AS DOUBLE) > 0.5
                and TRY_CAST(attributes['AC'] AS INTEGER) > 100
            </example_use>
        </column>
        <column>
            <column_name>attributes</column_name>
            <column_description>
                The attributes column in the gnomAD data typically contains a variety of annotations and metadata about each genetic
                variant. These attributes provide detailed information on the variant's properties, including its functional impact,
                frequency in different populations, quality metrics, and other relevant data points. Below is an explanation of some
                common attributes you might find in this column. The attributes in GenomAD data are:
                
                `AC`: Allele Count. Definition: The number of times the alternate allele is observed in the dataset. Purpose: Provides 
                insight into how common a variant is in the population.
                
                `AF`: Allele Frequency. Definition: The frequency of the alternate allele in the dataset. Purpose: Indicates how 
                common or rare a variant is in the population. 
            </column_description>
            <example_use>
                select * from genomad
                where TRY_CAST(attributes['AF'] AS DOUBLE) > 0.5
                and TRY_CAST(attributes['AC'] AS INTEGER) > 100
            </example_use>
        </column>
    </table>
"""
variants_prompt = """
    <table>
        <table_name>
        variants
        </table_name>
        <table_description>
        This table contains information about genetic variants.
        </table_description>

        <column>
            <column_name>contigname</column_name>
            <column_description>
                This column specifies the name of the contig (a contiguous sequence of DNA) or chromosome where the variant is located.
                It is typically prefixed with "chr". If the user asks for variants at the chromossome 22, use `chr22` to access variants
                in this table.
            </column_description>
            <example_use>
                select *
                from variants
                where contigname = 'chr22'
                and start between 45509414 and 45509418;
            </example_use>
        </column>
        <column>
            <column_name>start</column_name>
            <column_description>
                The start position of the variant on the chromosome. This should be used to compose the primary key of the variant,
                along with the following tables: `contigname`, `end`, `referenceallele`, `alternatealleles`.
            </column_description>
            <example_use>
              SELECT * FROM variants WHERE start > 100000 and end < 200000;
            </example_use>
        </column>
        <column>
            <column_name>end</column_name>
            <column_description>
                The end position of the variant on the chromosome. This should be used to compose the primary key of the variant,
                along with the following tables: `contigname`, `start`, `referenceallele`, `alternatealleles`.
            </column_description>
            <example_use>
              SELECT * FROM variants WHERE and start > 100000 and end < 200000;
            </example_use>
        </column>
        <column>
            <column_name>referenceallele</column_name>
            <column_description>The reference allele of the variant</column_description>
            <example_use>
              SELECT * FROM variants WHERE referenceallele = 'XXXXXXXXXXXXXXX';
            </example_use>
        </column>
        <column>
            <column_name>alternatealleles</column_name>
            <column_description>An array of alternate alleles for the variant</column_description>
            <example_use>
                SELECT * FROM variants
                cross join unnest(alternatealleles) as t(alternateallele)
                where alternateallele in ('G', 'T');
            </example_use>
        </column>
        <column>
            <column_name>qual</column_name>
            <column_description>The quality score of the variant, typically a Phred-scaled score indicating the confidence in the variant call.</column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE qual > 30;
            </example_use>
        </column>
        <column>
            <column_name>filters</column_name>
            <column_description>
                The filter status of a variant in the gnomAD dataset indicates whether the variant has passed quality 
                control filters. Variants that do not pass certain thresholds for quality metrics are flagged with 
                specific filter labels. Here are some common filter statuses you might encounter in gnomAD data:

                `PASS`: The variant has passed all quality control filters.
                `RF`: Random Forest filter indicating that the variant did not meet the thresholds set by a random forest classifier used to distinguish true variants from sequencing artifacts.
                `AC0`: Allele Count 0 filter indicating that the variant has zero allele counts after filtering out low confidence genotypes.
                `InbreedingCoeff`: Inbreeding Coefficient filter indicating that the variant has an inbreeding coefficient less than -0.3, suggesting possible genotyping errors.
                `AS_VQSR`: Allele-Specific Variant Quality Score Recalibration filter is a filter status applied to variants based on a statistical model that recalibrates the variant quality scores. This process involves constructing a model that differentiates between true variants and sequencing artifacts using known variant sites and a set of quality metrics. 
            
                These filters help ensure the reliability of the data used for downstream analyses.
            </column_description>
            <example_use>
                select * from variants
                    cross join unnest(filters) as t(filter)
                WHERE filter NOT LIKE '%AC0%'
                AND start between 128401319 and 129401319;
            </example_use>
        </column>
        <column>
            <column_name>qual</column_name>
            <column_description>The quality score of the variant, typically a Phred-scaled score indicating the confidence in the variant call.</column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE qual > 30;
            </example_use>
        </column>
        <column>
            <column_name>splitfrommultiallelic</column_name>
            <column_description>
                Multi-allelic Sites: These are genomic positions where more than one type of mutation (alternate allele) occurs. For example, at a given position, the reference allele might be A, and the alternate alleles might be T and G.
                Splitting Process: During the variant calling process, tools like GATK can split multi-allelic sites into multiple bi-allelic records. This means that instead of having a single record with multiple alternate alleles, there will be multiple records each with one alternate allele.
                Purpose of `splitfrommultiallelic`: This field indicates whether a variant record was created as a result of this splitting process. It helps users understand that the variant was originally part of a more complex multi-allelic site.
            </column_description>
            <example_use>
                select * from variants
                where splitfrommultiallelic = false
                AND start between 129401219 and 129401329;
            </example_use>
        </column>
        <column>
            <column_name>attributes</column_name>
            <column_description>
                typically contains a variety of key-value pairs that provide additional information about each variant. Here are some of the possible keys you might encounter in this column:
                callable: Indicates the callable regions from specific sequencing datasets. For example the value: `CS_CCS15kb_20kbDV_callable,CS_CCS15kb_20kbGATK4_callable` refers to regions callable in datasets produced by CCS (Circular Consensus Sequencing) at 15kb-20kb read lengths using Deep Variant (DV) and GATK4 algorithms.

                datasetsmissingcall: Lists the datasets that do not have calls for this variant. For example `IonExome,SolidSE75bp`: Indicates that the IonExome and SolidSE75bp datasets do not have calls for this variant.
                
                platformnames: Lists the sequencing platforms used. For example `PacBio,Illumina,10X,CG`: Indicates the sequencing platforms Pacific Biosciences (PacBio), Illumina, 10X Genomics (10X), and Complete Genomics (CG) were used.
                
                datasets: The total number of datasets. For example 4: Indicates there are 4 datasets.
                
                callsetnames: Lists the names of the callsets used for the variant. For example `CCS15kb_20kbDV,CCS15kb_20kbGATK4,HiSeqPE300xGATK,10XLRGATK,CGnormal,HiSeqPE300xfreebayes`: Specifies the different callsets, which include:
                        CCS15kb_20kb with Deep Variant (DV)
                        CCS15kb_20kb with GATK4
                        HiSeq paired-end 300x with GATK
                        10X Long Read with GATK
                        CG normal
                        HiSeq paired-end 300x with FreeBayes
                
                datasetnames: Lists the names of the datasets used for the variant. For example `CCS15kb_20kb,HiSeqPE300x,10XChromiumLR,CGnormal`: Indicates the dataset names, including:
                        CCS15kb_20kb (Circular Consensus Sequencing with 15kb-20kb read lengths)
                        HiSeq paired-end 300x
                        10X Chromium Long Read (LR)
                        CG normal
                
                callsets: The total number of callsets. For example `6`: Indicates there are 6 callsets.
                
                difficultregion: Lists the difficult regions where the variant is found. For example `HG001.hg38.300x.bam.bilkentuniv.010920.dups,hg38.segdups_sorted_merged,lowmappabilityall`: Specifies the difficult regions:
                        HG001.hg38.300x.bam.bilkentuniv.010920.dups: Regions in HG001 sample with 300x coverage, marked as duplicates by Bilkent University.
                        hg38.segdups_sorted_merged: Segmented duplications in the hg38 reference genome.
                        lowmappabilityall: Regions with low mappability in all datasets.
                
                platforms: The total number of platforms used. For example `4`: Indicates there are 4 platforms used.
            </column_description>
            <example_use>
                select *
                from variants
                where attributes['callable']='CS_CCS15kb_20kbDV_callable,CS_CCS15kb_20kbGATK4_callable'
            </example_use>
        </column>
        <column>
            <column_name>phased</column_name>
            <column_description>
                A flag indicating whether the variant call is phased, meaning the two alleles are assigned to their respective haplotypes.
            </column_description>
            <example_use>
                select * from variants
                where phased = false
            </example_use>
        </column>
        <column>
            <column_name>alleledepths</column_name>
            <column_description>
                The depth of reads supporting each allele for each sample. This includes the number of reads that 
                support the reference allele and each alternate allele. The alleledepths column might contain values in 
                the format 10,5 where the first number is the depth for the reference allele and the second number is
                 for the alternate allele. Use the notation `alleledepths[1]` if you are interested in the depth of the 
                 reference allele or `alleledepths[2]` if you are interested in the depth of the alternate allele.
            </column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE alleledepths[2] > 250;
            </example_use>
        </column>
        <column>
            <column_name>conditionalquality</column_name>
            <column_description>
                A measure of the quality of the variant call, conditional on the data observed.
            </column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE conditionalquality > 250;
            </example_use>
        </column>
        <column>
            <column_name>spl</column_name>
            <column_description>
                Sample-specific information for each variant call, such as sample ID and specific genotype data.
            </column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE spl = 'HG001';
            </example_use>
        </column>
        <column>
            <column_name>depth</column_name>
            <column_description>
                The total depth of coverage at the variant position, across all samples.
            </column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE depth > 500;
            </example_use>
        </column>
        <column>
            <column_name>sampleid</column_name>
            <column_description>
                The unique identifier for each sample.
            </column_description>
            <example_use>
                SELECT *
                FROM variants
                WHERE sampleid = 'HG001';
            </example_use>
        </column>
    </table>
"""
clinvar_prompt= """
<table>
        <table_name>
            clinvar
        </table_name>
        <table_description>
            The ClinVar table refers to the structured data available in ClinVar, a freely accessible public archive for 
            reports of the relationships among human genetic variations and phenotypes, along with supporting evidence.
            ClinVar is a freely accessible, public archive of reports of human variations classified for diseases and
            drug responses, with supporting evidence. ClinVar thus facilitates access to and communication about the 
            relationships asserted between human variation and observed conditions, and the history of those assertions. 
            ClinVar processes submissions reporting variants found in patient samples, classifications for diseases and 
            drug responses, information about the submitter, and other supporting data.
        </table_description>

        <column>
            <column_name>contigname</column_name>
            <column_description>
                This column specifies the name of the contig (a contiguous sequence of DNA) or chromosome where the 
                variant is located. It is typically prefixed with "chr". If the user asks for variants at the 
                chromosome 22, use the integer `22` to access variants in this table, between position 43044295 and 
                43125364
            </column_description>
            <example_use>
                select *
                from clinvar
                where contigname = '22'
                and start between 43044295 AND 43125364
            </example_use>
        </column>
        <column>
            <column_name>start</column_name>
            <column_description>
                The start position of the variant on the chromosome. This should be used to compose the primary key of 
                the variant, along with the following tables: `contigname`, `"end"`, `referenceallele`, `alternatealleles`.
            </column_description>
            <example_use>
              SELECT * FROM clinvar WHERE start > 100000 and "end" < 200000;
            </example_use>
        </column>
        <column>
            <column_name>end</column_name>
            <column_description>
                The end position of the variant on the chromosome. This should be used to compose the primary key of the variant,
                along with the following tables: `contigname`, `start`, `"end"`, `referenceallele`, `alternatealleles`.
            </column_description>
            <example_use>
              SELECT * FROM clinvar WHERE and start > 100000 and end < 200000;
            </example_use>
        </column>
        <column>
            <column_name>referenceallele</column_name>
            <column_description>The reference allele of the variant.</column_description>
            <example_use>
              SELECT * FROM clinvar WHERE referenceallele = 'XXXXXXXXXXXXXXX';
            </example_use>
        </column>
        <column>
            <column_name>alternatealleles</column_name>
            <column_description>An array of alternate alleles for the variant</column_description>
            <example_use>
                SELECT * FROM clinvar
                cross join unnest(alternatealleles) as t(alternateallele)
                where alternateallele in ('G', 'T');
            </example_use>
        </column>
        <column>
            <column_name>qual</column_name>
            <column_description>The quality score of the variant, typically a Phred-scaled score indicating the confidence in the variant call.</column_description>
            <example_use>
                SELECT *
                FROM clinvar
                WHERE qual > 30;
            </example_use>
        </column>
        <column>
            <column_name>attributes</column_name>
            <column_description>
                This is the main column of this table. The attributes column in ClinVar provides a wealth of information 
                about the genetic variant, including its type, clinical significance, molecular effect, associated 
                conditions, and the gene involved. This structured data helps clinicians and researchers interpret the 
                potential impact of variants on health. The attribute column is a `map(65535)` data type, which allows
                for flexible storage of key-value pairs. The keys are strings, and the values can be of various data 
                types. Below is a description of each available attribute:
                
                <attribute>
                    <attribute_name>CLNVC</attribute_name>
                    <attribute_description>
                        The variant is classified as a single nucleotide variant (SNV), indicating a substitution of one nucleotide for another in the DNA sequence.
                    </attribute_description>
                    <attribute_example>CLNVC=single_nucleotide_variant</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>RS</attribute_name>
                    <attribute_description>
                        This is the Reference SNP ID number (RSID) from the dbSNP database, uniquely identifying the specific variant.
                    </attribute_description>
                    <attribute_example>RS=121434568</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>CLNDISDB</attribute_name>
                    <attribute_description>
                        This attribute lists the identifiers for the conditions or phenotypes associated with the variant across multiple medical databases. For example, Human Phenotype Ontology (HPO), MONDO, MeSH, MedGen, and SNOMED CT provide corresponding condition codes. These codes help standardize and reference diseases and phenotypes across various systems.
                    </attribute_description>
                    <attribute_example>
                        CLNDISDB=Human_Phenotype_Ontology:HP:0030078,MONDO:MONDO:0005061,MeSH:D000077192,MedGen:C0152013|Human_Phenotype_Ontology:HP:0030358,MONDO:MONDO:0005233,MeSH:D002289,MedGen:C0007131,SNOMED_CT:254637007|MONDO:MONDO:0005138,MedGen:C0684249|MedGen:C1851577|MedGen:C4016032|MedGen:CN077981|MedGen:CN077987|MedGen:CN225347|MedGen:CN315865
                    </attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>CLNSIG</attribute_name>
                    <attribute_description>
                        The clinical significance of the variant is classified as "drug response," indicating that the variant affects a patient's response to certain medications (e.g., efficacy or resistance).
                    </attribute_description>
                    <attribute_example>CLNSIG=drug_response</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>GENEINFO</attribute_name>
                    <attribute_description>
                        This is the Sequence Ontology term that describes the type of variation. SO:0001483 corresponds to a specific classification in the Sequence Ontology.
                    </attribute_description>
                    <attribute_example>CLNVCSO=SO:0001483</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>CLNVI</attribute_name>
                    <attribute_description>
                        This field links the variant to records in PharmGKB, a database that provides information on how human genetic variations affect drug responses. It also references data from UniProtKB and OMIM, giving more detailed annotation on the variant's effect at the protein and clinical levels.
                    </attribute_description>
                    <attribute_example>CLNVI=PharmGKB:981420042|PharmGKB_Clinical_Annotation:981475838|PharmGKB_Clinical_Annotation:981475880|PharmGKB_Clinical_Annotation:981420042|UniProtKB_(protein):P00533#VAR_019298|PharmGKB:981475838|PharmGKB:981420042PA131301952|PharmGKB:981475880|PharmGKB:981475838PA134687924|OMIM_Allelic_Variant:131550.0002</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>ORIGIN</attribute_name>
                    <attribute_description>
                        The origin of the variant is categorized as 3, which usually refers to a somatic origin. Somatic variants are not inherited but arise in certain cells and can lead to diseases like cancer.
                    </attribute_description>
                    <attribute_example>ORIGIN=3</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>MC</attribute_name>
                    <attribute_description>
                        This attribute provides the molecular consequence of the variant. SO:0001583 indicates a missense variant, where a single nucleotide change results in a different amino acid being produced in the protein.
                    </attribute_description>
                    <attribute_example>MC=SO:0001583|missense_variant</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>CLNREVSTAT</attribute_name>
                    <attribute_description>
                        The clinical significance classification has been reviewed by an expert panel, indicating a higher level of confidence in the interpretation compared to single-submitter data.
                    </attribute_description>
                    <attribute_example>CLNREVSTAT=reviewed_by_expert_panel</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>CLNDN</attribute_name>
                    <attribute_description>
                        This attribute lists the disease names associated with the variant, such as lung adenocarcinoma, non-small cell lung carcinoma, and responses to tyrosine kinase inhibitors like erlotinib and gefitinib. It highlights that the variant influences how patients with these cancers respond to specific treatments.
                    </attribute_description>
                    <attribute_example>CLNDN=Lung_adenocarcinoma|Non-small_cell_lung_carcinoma|Lung_carcinoma|Adenocarcinoma_of_lung,_response_to_tyrosine_kinase_inhibitor_in,_somatic|Nonsmall_cell_lung_cancer,_response_to_tyrosine_kinase_inhibitor_in,_somatic|Erlotinib_response|Gefitinib_response|Tyrosine_kinase_inhibitor_response|gefitinib_response_-_Efficacy</attribute_example>
                    <sql_example>
                        SELECT
                            concat('chr', c.contigname) as contigname,
                            c.start,
                            c.referenceallele,
                            c.alternatealleles,
                            c.attributes,
                            c.attributes['GENEINFO'] as gene_info,
                            c.attributes['CLNSIG'] as clinical_significance,
                            c.attributes['CLNDN'] as disease_name,
                            c.sampleid,
                            g."names",
                            g.attributes,
                            g.contigname as contigname_genomad,
                            g."start",
                            g.sampleid
                        from omicsdb.clinvar c
                        LEFT JOIN omicsdb.genomad g on c."end" = g."end" AND g.contigname = concat('chr', c.contigname)
                        where 1=1
                            and c.attributes['CLNDN'] like '%Non-small_cell_lung_carcinoma%'
                            and c.attributes['CLNSIG'] in ('drug_response')
                    </sql_example>
                </attribute>
                <attribute>
                    <attribute_name>ALLELEID</attribute_name>
                    <attribute_description>
                        This is a unique identifier assigned to the allele in ClinVar. It distinguishes this specific allele from others within the database.
                    </attribute_description>
                    <attribute_example>ALLELEID=31648</attribute_example>
                </attribute>
                <attribute>
                    <attribute_name>CLNHGVS</attribute_name>
                    <attribute_description>
                        This is the HGVS (Human Genome Variation Society) nomenclature for the variant, describing that on chromosome 7 (NC_000007.14), at position 55,191,822, a thymine (T) has been replaced by guanine (G).
                    </attribute_description>
                    <attribute_example>CLNHGVS=NC_000007.14:g.55191822T>G</attribute_example>
                </attribute>
            </column_description>
            <example_use>
                SELECT
                            concat('chr', c.contigname) as contigname,
                            c.start,
                            c.referenceallele,
                            c.alternatealleles,
                            c.attributes,
                            c.attributes['GENEINFO'] as gene_info,
                            c.attributes['CLNSIG'] as clinical_significance,
                            c.attributes['CLNDN'] as disease_name,
                            c.sampleid,
                            g."names",
                            g.attributes,
                            g.contigname as contigname_genomad,
                            g."start",
                            g.sampleid
                        from omicsdb.clinvar c
                        LEFT JOIN omicsdb.genomad g on c."end" = g."end" AND g.contigname = concat('chr', c.contigname)
                        where 1=1
                            and c.attributes['CLNDN'] like '%Non-small_cell_lung_carcinoma%'
                            and c.attributes['CLNSIG'] in ('drug_response')
            </example_use>
        </column>
"""