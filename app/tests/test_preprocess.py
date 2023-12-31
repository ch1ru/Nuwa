from streamlit.testing.v1 import AppTest
import streamlit as st
import time
import os

from utils.AdataState import AdataState
from models.AdataModel import AdataModel
from utils.AdataState import AdataState
from models.AdataModel import AdataModel
from models.WorkspaceModel import WorkspaceModel
from database.database import SessionLocal
from sqlalchemy.orm import Session
from database.schemas import schemas
from utils.AdataState import AdataState

import scanpy as sc

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Test_Preprocess:
    def __init__(self, session_state = None):
        print(f"{bcolors.OKBLUE}Initialising page... {bcolors.ENDC}", end="")
        self.at = AppTest.from_file("pages/2_Preprocess.py")
        self.conn: Session = SessionLocal()
        if session_state is not None:
            self.at.session_state = session_state
            
        self.at.run(timeout=500)
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_add_and_delete_adata()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_notes()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_filter_highest_expressed()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_normalize_data()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_highest_variable_genes()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_filter_cells()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_filter_genes()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_pp_recipe()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_annot_mito()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_annot_ribo()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_annot_hb()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_batch_effect_removal_and_pca()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_doublet_prediction()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_scale_data()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_sampling_data()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_measure_gene_counts()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_remove_genes()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_regress_out()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        self.test_save_adata()
        assert not self.at.exception
        print(f"{bcolors.OKGREEN}OK{bcolors.ENDC}")
        
        
        
        
    def test_add_and_delete_adata(self):
        print(f"{bcolors.OKBLUE}test_add_and_delete_data {bcolors.ENDC}", end="")
        self.at.text_input(key="ti_new_adata_name").input("adata_test")
        self.at.text_input(key="ti_new_adata_notes").input("test_note")
        self.at.button(key="btn_add_adata").click().run(timeout=100)
        #test added to db
        assert self.conn.query(schemas.Adata).filter(schemas.Adata.adata_name == "adata_test") \
        .filter(schemas.Adata.notes == "test_note") \
        .filter(schemas.Adata.work_id == self.at.session_state.current_workspace.id).count() == 1
        #switch adata
        self.at.selectbox(key="sb_adata_selection").select("adata_test").run(timeout=100)
        #test notes
        assert self.at.text_area(key="sidebar_notes").value == "test_note"
        #test delete adata
        self.at.button(key="btn_delete_adata").click().run(timeout=100)
        assert self.conn.query(schemas.Adata).filter(schemas.Adata.adata_name == "adata_test") \
        .filter(schemas.Adata.notes == "test_note") \
        .filter(schemas.Adata.work_id == self.at.session_state.current_workspace.id).count() == 0
        #Select original adata
        self.at.selectbox(key="sb_adata_selection").select("mouse_mammary_epithelial").run(timeout=100)
        
    def test_filter_highest_expressed(self):
        print(f"{bcolors.OKBLUE}test_filter_highest_expressed {bcolors.ENDC}", end="")
        self.at.number_input(key="n_top_genes").increment() #increase to 21
        self.at.button(key="FormSubmitter:form_highest_expr-Filter").click().run(timeout=100)
        #TODO: Find a way to test if top genes are correct
        
    def test_highest_variable_genes(self):
        print(f"{bcolors.OKBLUE}test_highest_variable_genes {bcolors.ENDC}", end="")
        self.at.number_input(key="input_highly_variable_min_mean").set_value(0.0125)
        self.at.number_input(key="input_highly_variable_max_mean").set_value(3.00)
        self.at.button(key="FormSubmitter:form_highly_variable-Filter").click().run(timeout=100)
        adata = sc.read_h5ad('/app/data/bct_raw.h5ad')
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)
        sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
        for i, item in enumerate(adata.var.highly_variable):
            assert item == self.at.session_state.adata_state.current.adata.var.highly_variable[i]
        
    def test_filter_cells(self):
        print(f"{bcolors.OKBLUE}test_filter_cells {bcolors.ENDC}", end="")
        self.at.number_input(key="filter_cell_min_genes").set_value(200)
        #TODO: add other inputs
        self.at.button(key="FormSubmitter:form_filter_cells-Apply").click().run(timeout=100)
        #test filter
        adata = sc.read_h5ad('/app/data/bct_raw.h5ad')
        assert len(adata.obs) == 9288 #original obs
        sc.pp.filter_cells(adata, min_genes=200)
        assert len(self.at.session_state.adata_state.current.adata.obs) == len(adata.obs) #8573
        assert len(self.at.session_state.adata_state.current.adata.var) == len(adata.var) #1222
        from_file_adata = sc.read(self.at.session_state.adata_state.current.filename)
        assert len(from_file_adata.var) == len(adata.var)
        assert len(from_file_adata.obs) == len(adata.obs)
        
    def test_filter_genes(self):
        print(f"{bcolors.OKBLUE}test_filter_genes {bcolors.ENDC}", end="")
        self.at.number_input(key="filter_gene_min_cells").set_value(900)
        self.at.button(key="FormSubmitter:form_filter_genes-Apply").click().run(timeout=100)
        #use values from last filter
        assert len(self.at.session_state.adata_state.current.adata.obs) == 8573
        assert len(self.at.session_state.adata_state.current.adata.var) == 1169
        from_file_adata = sc.read(self.at.session_state.adata_state.current.filename)
        assert len(from_file_adata.var) == 1169
        assert len(from_file_adata.obs) == 8573
        
    def test_pp_recipe(self):
        print(f"{bcolors.OKBLUE}test_pp_recipe {bcolors.ENDC}", end="")
        self.at.selectbox(key="sb_pp_recipe").select("Seurat")
        self.at.button(key="FormSubmitter:form_recipes-Apply").click().run(timeout=100)
        
    def test_doublet_prediction(self):
        print(f"{bcolors.OKBLUE}test_doublet_prediction {bcolors.ENDC}", end="")
        self.at.number_input(key="ni_sim_doublet_ratio").set_value(2)
        self.at.number_input(key="ni_expected_doublet_rate").set_value(0.05)
        self.at.button(key="FormSubmitter:scrublet_form-Filter").click().run(timeout=100)
        
    def test_annot_mito(self):
        print(f"{bcolors.OKBLUE}test_annot_mito {bcolors.ENDC}", end="")
        self.at.number_input(key="ni_pct_counts_mt").set_value(5)
        self.at.button(key="FormSubmitter:form_annotate_mito-Apply").click().run(timeout=100)
        
    def test_annot_ribo(self):
        print(f"{bcolors.OKBLUE}test_annot_ribo {bcolors.ENDC}", end="")
        self.at.number_input(key="ni_pct_counts_ribo").set_value(5)
        self.at.button(key="FormSubmitter:form_annotate_ribo-Apply").click().run(timeout=100)
        
    def test_annot_hb(self):
        print(f"{bcolors.OKBLUE}test_annot_hb {bcolors.ENDC}", end="")
        
    def test_measure_gene_counts(self):
        print(f"{bcolors.OKBLUE}test_measure_gene_counts {bcolors.ENDC}", end="")
        
    def test_remove_genes(self):
        print(f"{bcolors.OKBLUE}test_remove_genes {bcolors.ENDC}", end="")
        
    def test_regress_out(self):
        print(f"{bcolors.OKBLUE}test_regress_out {bcolors.ENDC}", end="")
        
    def test_normalize_data(self):
        print(f"{bcolors.OKBLUE}test_normalize_data {bcolors.ENDC}", end="")
        #normalize total
        self.at.number_input(key="ni_target_sum").set_value(1)
        self.at.button(key="FormSubmitter:form_normalize_total-Apply").click().run(timeout=100)
        assert int(self.at.session_state.adata_state.current.adata.to_df().iloc[:, :].values.sum()) == len(self.at.session_state.adata_state.current.adata.obs)
        from_file_adata = sc.read(self.at.session_state.adata_state.current.filename)
        assert int(from_file_adata.to_df().iloc[:, :].values.sum()) == int(len(from_file_adata.obs))
        #TODO: add per cell normalize test

        
    def test_notes(self):
        print(f"{bcolors.OKBLUE}test_notes {bcolors.ENDC}", end="")
        self.at.selectbox(key="sb_adata_selection").select("mouse_mammary_epithelial").run(timeout=150)
        self.at.text_area(key="sidebar_notes").input("Important notes").run(timeout=150)
        adata = self.conn.query(schemas.Adata).filter(schemas.Adata.adata_name == "mouse_mammary_epithelial") \
        .filter(schemas.Adata.work_id == self.at.session_state.current_workspace.id).first()
        assert adata.notes == "Important notes"
        self.at.selectbox(key="sb_adata_selection").select("mouse_mammary_epithelial").run(timeout=150)
        assert self.at.text_area(key="sidebar_notes").value == "Important notes"
        
    def test_save_adata(self):
        print(f"{bcolors.OKBLUE}test_save_adata {bcolors.ENDC}", end="")
        self.at.selectbox(key="sb_adata_selection").select("mouse_mammary_epithelial").run(timeout=150)
        self.at.button(key="btn_save_adata").click().run(timeout=100)
        assert os.path.isfile(os.path.join(os.getenv('WORKDIR'), 'downloads', 'mouse_mammary_epithelial', 'mouse_mammary_epithelial.h5ad'))
        downloaded_adata = sc.read_h5ad(os.path.join(os.getenv('WORKDIR'), 'downloads', 'mouse_mammary_epithelial', 'mouse_mammary_epithelial.h5ad'))
        current_adata = sc.read_h5ad(os.path.join(os.getenv('WORKDIR'), 'adata', 'mouse_mammary_epithelial.h5ad'))
        #test seurat format
        self.at.checkbox(key="cb_seurat_format").check().run(timeout=100)
        self.at.button(key="btn_save_adata").click().run(timeout=500)
        assert os.path.isfile(os.path.join(os.getenv('WORKDIR'), 'downloads', 'mouse_mammary_epithelial', 'seurat', 'barcodes.tsv'))
        assert os.path.isfile(os.path.join(os.getenv('WORKDIR'), 'downloads', 'mouse_mammary_epithelial', 'seurat', 'features.tsv'))
        assert os.path.isfile(os.path.join(os.getenv('WORKDIR'), 'downloads', 'mouse_mammary_epithelial', 'seurat', 'matrix.mtx'))
        assert os.path.isfile(os.path.join(os.getenv('WORKDIR'), 'downloads', 'mouse_mammary_epithelial', 'seurat', 'metadata.csv'))
        
        
    def test_scale_data(self):
        print(f"{bcolors.OKBLUE}test_scale_adata {bcolors.ENDC}", end="")
        
    def test_batch_effect_removal_and_pca(self):
        print(f"{bcolors.OKBLUE}test_batch_effect_removal_and_adata {bcolors.ENDC}", end="")
        adata_original = self.at.session_state.adata_state.current.adata
        sc.pp.combat(adata_original, key='BATCH', inplace=False)
        sc.pp.pca(adata_original)
        self.at.selectbox(key="sb_batch_effect_key").select("BATCH")
        self.at.button(key="FormSubmitter:batch_effect_removal_form-Apply").click().run(timeout=500)
        assert adata_original.obsm['X_pca'].all() == self.at.session_state.adata_state.current.adata.obsm['X_pca'].all() #TODO: make sure this works
        
        
    def test_sampling_data(self):
        print(f"{bcolors.OKBLUE}test_sampling_adata {bcolors.ENDC}", end="")

    def get_final_session_state(self):
        return self.at.session_state
    
        





        