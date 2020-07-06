import os
import sys
import re

import chlamdb

from Bio import SeqIO

def parse_orthofinder_output_file(output_file):
    protein_id2orthogroup_id = {}
    parsing = open(output_file, 'r')

    for group, line in enumerate(parsing):
        tokens = line.strip().split(' ')[1:]
        for locus in tokens:
            protein_id2orthogroup_id[locus] = group
    return protein_id2orthogroup_id

# TODO: import the two following functions into the chlamdb file to remove
# all database code from this file
def setup_biodb(kwargs):
    sqlpsw = os.environ['SQLPSW']
    db_type = kwargs["chlamdb.db_type"]
    db_name = kwargs["chlamdb.db_name"]
    schema_dir = kwargs["chlamdb.biosql_schema_dir"]
    err_code = 0

    if db_type=="sqlite":
        import sqlite3
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        url_biosql_scheme = 'biosqldb-sqlite.sql'
        err_code = os.system(f"sqlite3 {db_name} < {schema_dir}/{url_biosql_scheme}")
    else:
        import MySQLdb
        conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                                    user="root", # your username
                                    passwd=sqlpsw) # name of the data base
        cursor = conn.cursor()
        sql_db = f'CREATE DATABASE IF NOT EXISTS {db_name};'
        cursor.execute(sql_db,)
        conn.commit()
        cursor.execute(f"use {db_name};",)
        url_biosql_scheme = 'biosqldb-mysql.sql'
        err_code = os.system(f"mysql -uroot -p{sqlpsw} {db_name} < {schema_dir}/{url_biosql_scheme}")

    # not really logical to me, but creating a database
    # from the biosql is necessary
    db = chlamdb.DB.load_db(kwargs)
    db.create_biosql_database(kwargs)
    db.commit()
    if err_code != 0:
        raise IOError("Problem loading sql schema:", err_code)

def create_data_table(kwargs):
    db_type = kwargs["chlamdb.db_type"]
    db_name = kwargs["chlamdb.db_name"]
    if db_type=="sqlite":
        import sqlite3
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
    else:
        import os
        import MySQLdb
        sqlpsw = os.environ['SQLPSW']

        conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                                    user="root", # your username
                                    passwd=sqlpsw, # your password
                                    db=db_name) # name of the data base
        cursor = conn.cursor()
    entry_list = [
        ("gbk_files", "mandatory", False),
        ("orthology_data", "mandatory", False),
        ("orthology_comparative", "mandatory", False),
        ("orthology_comparative_accession", "mandatory", False),
        ("orthology_consensus_annotation", "mandatory", False),
        ("orthogroup_alignments", "mandatory", False),
        ("old_locus_table", "mandatory", False),
        ("reference_phylogeny", "mandatory", False),
        ("taxonomy_table", "mandatory", False),
        ("genome_statistics", "mandatory", False),
        ("BLAST_database", "optional", False),
        ("gene_phylogenies", "optional", False),
        ("interpro_data", "optional", False),
        ("interpro_comparative", "optional", False),
        ("interpro_comparative_accession", "optional", False),
        ("priam_data", "optional", False),
        ("priam_comparative", "optional", False),
        ("priam_comparative_accession", "optional", False),
        ("COG_data", "optional", False),
        ("COG_comparative", "optional", False),
        ("COG_comparative_accession", "optional", False),
        ("KEGG_data", "optional", False),
        ("KEGG_comparative", "optional", False),
        ("KEGG_comparative_accession", "optional", False),
        ("pfam_comparative", "optional", False),
        ("pfam_comparative_accession", "optional", False),       
        ("TCDB_data", "optional", False),
        ("psortb_data", "optional", False),
        ("T3SS_data", "optional", False),
        ("PDB_data", "optional", False),
        ("BLAST_refseq", "optional", False),
        ("BLAST_swissprot", "optional", False),
        ("BBH_phylogenies", "optional", False),
        ("GC_statistics", "optional", False),
        ("gene_clusters", "optional", False),
        ("phylogenetic_profile", "optional", False),
        ("synonymous_table", "optional", False),
        ("interpro_taxonomy", "optional", False), # interpro taxnonomy statistics
        ("pfam_taxonomy", "optional", False), #  taxnonomy statistics
        ("COG_taxonomy", "optional", False) # COG taxnonomy statistics
    ]
    
    sql = 'create table biodb_config (name varchar(200), type varchar(200), status BOOLEAN)'
    
    cursor.execute(sql)
    conn.commit()
    
    sql = 'insert into biodb_config values ("%s", "%s", %s)'
    for row in entry_list:
        cursor.execute(sql % (row[0], row[1], row[2]),)
    conn.commit()
    
def insert_gbk(db, one_gbk):
    input_file = open(one_gbk, "r")
    records = SeqIO.parse(input_file, 'genbank')
    for record in records:
        params = {}
        params["accession"] = record.id.split('.')[0]
        params["taxon_id"] = db.get_taxid_from_accession(params["accession"])
        for feature in record.features:
            if feature.type == 'CDS' and not 'pseudo' in feature.qualifiers:
                params["start"] = re.sub('>|<','', str(feature.location.start))
                params["end"] = re.sub('>|<','', str(feature.location.end))
                params["strand"] = feature.strand
                params["gene"] = feature.qualifiers.get("gene", ['-'])[0]
                params["product"] = feature.qualifiers.get("product", ['-'])[0]
                params["locus_tag"] = feature.qualifiers["locus_tag"][0]
                params["old_locus_tag"] = feature.qualifiers.get("old_locus_tag", [False])[0]
                params["protein_id"] = feature.qualifiers.get("protein_id", ['.'])[0]
                params["translation"] = feature.qualifiers.get("translation", ['-'])[0]
                db.insert_cds(params)
            elif feature.type == 'rRNA':
                params["start"] = re.sub('>|<','', str(feature.location.start))
                params["end"] = re.sub('>|<','', str(feature.location.end))
                params["strand"] = feature.strand
                params["product"] = feature.qualifiers.get("product", ["-"])[0]
                db.insert_rRNA_in_feature_table(params)

def setup_chlamdb(**kwargs):
    setup_biodb(kwargs)
    create_data_table(kwargs)

def load_gbk(gbks, args):
    db = chlamdb.DB.load_db(args)

    db.create_cds_tables()
    for gbk in gbks:
        records = [i for i in SeqIO.parse(gbk, 'genbank')]
        db.load_gbk_wrapper(records)
        assert(len(records) == 1)
        insert_gbk(db, gbk)
    db.set_status_in_config_table("gbk_files", 1)
    db.create_indices_on_cds()
    db.commit()


def load_orthofinder_results(orthofinder_output, args):
    db = chlamdb.DB.load_db(args)
    orthogroup_feature_id = db.setup_orthology_table()
    hsh_prot_to_group = parse_orthofinder_output_file(orthofinder_output)
    hsh_locus_to_feature_id = db.get_hsh_locus_to_seqfeature_id()
    db.add_orthogroups_to_seq(hsh_prot_to_group, hsh_locus_to_feature_id, orthogroup_feature_id)

    arr_cnt_tables = db.get_orthogroup_count_table()
    arr_taxon_ids = db.taxon_ids()

    db.create_orthology_table(arr_cnt_tables)
    db.load_orthology_table(arr_cnt_tables, arr_taxon_ids)
    # db.create_locus_to_feature_table()
    db.set_status_in_config_table("orthology_data", 1)
    db.commit()
