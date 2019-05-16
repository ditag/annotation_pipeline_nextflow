
# annotation pipeline (chlamdb-type database)

- blast each pairs of proteomes
- run orthoFinder
- extract orthogroups fasta
- align each orthogroup with mafft
- build phylogenies with iq-tree
- identify core single copy orthogroups
- concatenate core orthogroup alignments & build a reference phylogeny with FastTree
- rps-BLAST to COG database (cdd PSSM)
- BLASTp to swissprot database
- execute interproscan
- execute KofamScan to get KO annotation
- mapping to string, oma, pdb, tcdb databases (exact matches)
- get PMID mapping from string

# refseq reference/representative genomes

- [X] download representative/reference genomes from RefSeq database
- [ ] annotate each genome with InterproScan: TODO: use exact match to uniparc to get precomputed annotations, only execute interproscan for unannotated proteins OR simply annotate them separately (speed of iprlookup?)
- alternative option: work with uniprotkb proteomes 1) exclude anomalous proteomes based on refseq data 2) get species taxid for each proteome 3) remove redudancy (keep one prepresentative per species taxid) 4) retrieve interpro annotation from interproscan uniparc annotations
- [ ]make stats from ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt: superkingdom, annotated genomes,...
- [ ] annotate representative genomes with kofamscan => phylogenetic profile of KO, modules, pathways,...
- [ ] use GTDB rather than NCBI taxonomy? ==> does not include eukaryotes
  - [ ] see http://annotree.uwaterloo.ca/app/#/?qtype=pfam&qstring=PF00617&eval=0.00001
  - [ ] get leaf2phylum & leaf2order & leaf2class
  - [ ] extract subset of their reference phylogeny
  - [ ] get phylum tree & order tree & class tree (keep only lineages containing representative/reference genomes) (see how many different phylum, class, orders)

# DONE

- [X] input samples table1: genbank assembly accession
- [X] input samples table2: path to local faa files
- [X] parallelized BLASTp for orthofinder
- [X] orthofinder
- [X] alignments of each orthogroup with mafft
- [X] reconstruction of a phylogeny for orthogroups with more than 3 sequences with iq-tree
- [X] identify single copy orthogroups. Accept missing data (as parameter, default=0 missing data)
- [X] write core orthogroups with accessions as headers
- [X] concatenate core orthogroups
- [X] build phylogeny with fasttree
- [X] remove aa sequences reducancy before annotation (use sequence hash as seqid)
- [X] execute blast vs SwissProt for chunks of 1000 sequences
- [X] execute rpsblast vs COG for chunks of 1000 sequences
- [X] execute plast RefSeq for chunks of 1000 sequences
- [X] execute diamond RefSeq for chunks of 1000 sequences
- [X] execute interproscan by chunks of 1000 sequences
- [X] execute kofamscan by chunks of 1000 sequence (https://www.genome.jp/tools/kofamkoala/)
- [X] get mapping to uniparc (exact match)
- [X] get exact match to eggnog/string
- [X] get exact match to oma
- [X] get exact match to PDB
- [X] get PMID associations from string database for mapped seqs
- [X] execute gblast vs TCDB for chunks of 1000 sequences (only for unmapped sequences): todo: solve dependancies/env variables
- [X] interproscan: analyse separately uniparc matches from non matched entries (allocate more ressources to the later): no match: more ram (16go), and cores (8), no lookup service

# TODO

## priority 1


- [ ] extract best swissprot and refseq hits for each sequence (from database), build phylogeny with non-redundant set of BBH (x top seqs refseq + y top seqs swissprot as parameters)
  - [X] get taxid of hits => make protein_accession2phylum sqlite db
  - [ ] setup db (single process)
    - [X] load blast results into sqlite db
    - [X] load locus tag 2 hash table
    - [X] load orthology data into sqlite db (locus2orthogroup)
  - [ ] keep X hits/sequence filter out Chlamydiae/Planctomycetes,... hits (attach linear taxonomy)
  - [ ] retrieve aa sequences
  - [ ] generate one fasta files/orthogroup
  - [ ] align with mafft
  - [ ] build phylogeny
- [ ] retrieve GO annotations from uniprotKB GOA (exact match or best diamond/plast hit if no exact match?)
- [ ] retrieve uniprot annotation score for matched uniprotkb entries
- [ ] execute checkM

## priority 2

- [ ] execute T3 effector prediction: BPBAac
- [ ] execute T3 effector prediction: T3_MM
- [ ] execute T3 effector prediction: effective

- [ ] VF annotation with all databases

- [ ] retrieve DOORS2 operons

- [ ] mapping to uniprot proteomes: https://www.ebi.ac.uk/proteins/api/doc/#!/proteomes/search
- [ ] curl -X GET --header 'Accept:application/json' 'https://www.ebi.ac.uk/proteins/api/proteomes?offset=0&size=100&xref=GCA_000068525.2'

- [ ] match to uniparc: use https://www.ebi.ac.uk/proteins/api/doc/#!/uniparc/getBySequence
- [ ] get entire proteomes: https://www.ebi.ac.uk/proteins/api/doc/#!/uniparc/getByProteomeId

## development

- [ ] (retrieve uniprot annotation from uniprotKB (exact match or best diamond/plast hit if no exact match?))

- [ ] Resfams annotation

- [ ] execute macsyfinder for crispr
- [ ] execute macsyfinder for capsular genes
- [ ] execute macsyfinder for secretion systems

- [ ] Inc prediction based on bi-lobbed hydrophobic domains

- [ ] execute PRIAM for each genome or hmmsearch with PRIAM database?

- [ ] predict operons when not in doors? operon-mapper?

- [ ] run genome properties with interprocsn tsv files (https://genome-properties.readthedocs.io/en/latest/index.html, https://www.ebi.ac.uk/interpro/genomeproperties/)

- [ ] Carbohydrate-Active Enzyme database: http://csbl.bmb.uga.edu/dbCAN/

- [ ] PSORTb version 3.00

- [ ] get kegg annotation from eggnog, unpiprotKB extact or best match, eggnog

- [ ]  PMID mapping with ppaperBLAST http://papers.genomics.lbl.gov/cgi-bin/litSearch.cgi

# Web Interface

- [ ] add tcdb classification to "fam" (annotation, phylogenetic profile,...). Include all classification levels (superfamilies,...)
- [ ] idem with EC classification system
- [ ] integrate interpro hierarchy
- [ ] add explanations for hydropathy plot
- [ ] add download page (download KO mapping, interpro mapping, all phylogenies, orthology table,...)
- [ ] search bar: add option to search for TCDB accessions

## Ideas

- [ ] check if BioVx tools could be used to identitify candidate Incs
- [ ] https://www.uniprot.org/help/api_idmapping
- [ ] IS annotation with https://github.com/xiezhq/ISEScan (https://github.com/emrobe/SfB-course/blob/master/Deployment_wrapper.sh) or https://github.com/thanhleviet/ISfinder-sequences
- [ ] KO annotation: compare GHOSTKOALA with eggnog/uniprot annotations
- [ ] execute plast/mmseq2/diamond vs UNIREF90 for chunks of 1000 sequences?
- [ ] metacyc?
- [ ] exact match to COG betfore doing BLAST to reduce computations? => do not blast sequence that are in the COGdb (assign it directly)
- [ ] predict operons when not in doors?
- [ ] orthoDB
- [ ] ICEberg
- [ ] viruses: vFam (http://derisilab.ucsf.edu/software/vFam/)
- [ ] VirSorter (http://merenlab.org/2018/02/08/importing-virsorter-annotations/)
- [ ] https://widdowquinn.github.io/2018-03-06-ibioic/02-sequence_databases/09-KEGG_programming.html
- [ ] read BioV (gblat3) manual: transporter annotation, programmatic Interface with TCDB,...
- [ ] transporters https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0192851
- [ ] transporters https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0208151, https://www.nature.com/articles/nbt.4024
- [ ] use GTDB instead of NCBI taxonomy?
- [ ] phylogenetic profiling for pfam/interpro profiles with RefSeq data
- [ ] MCL BLAST graph vizualisation
- [ ] standardize annotation within orthogroups: if sufficient reciprocal seq coverage (BLAST align), expand KO, COG and EC annotations   
- [ ] curated blast db: https://msystems.asm.org/content/4/2/e00072-19

## Notes

- ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/bacsu.txt
- ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/dbxref.txt

- BLAST vs PLAST vs mmseq2 vs diamond: statisics and best hits comparisons
- install eggnog-mapper?
- execute eggnog-mapper and ghostkoala online?
- HHBLITS
