from test_preprocess import Test_Preprocess
from test_integrate import Test_Integrate
from test_dashboard import Test_Dashboard
from test_upload import Test_Upload
from test_create_model import Test_Create_Model
from test_train import Test_Train
from test_cluster_analysis import Test_Cluster_Analysis
from test_tranjectory_inference import Test_Trajectory_Inference
from test_spatial_transcriptomics import Test_Spatial_Transcriptomics
from test_terminal import Test_Terminal

from database.database import SessionLocal
from sqlalchemy.orm import Session
from utils.AdataState import AdataState
from database.schemas import schemas
from models.WorkspaceModel import WorkspaceModel
import os
import time
from random import randrange
import shutil
from datetime import datetime, date

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    conn: Session = SessionLocal()

    print()
    print(f"{bcolors.BOLD}===============Testing Dashboard===============")
    nonce = randrange(1, 10000000)
    dashboard_test = Test_Dashboard(workspace_nonce=nonce)
    dashboard_state = dashboard_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Upload pbmc3k===============")
    upload_test = Test_Upload(session_state=dashboard_state, dataset="mouse mammary epithelial")
    upload_state = upload_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Preprocess===============")
    pp_test = Test_Preprocess(session_state=upload_state)
    pp_state = pp_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Create Citeseq Model===============")
    create_model_test = Test_Create_Model(session_state=pp_state, model="Citeseq (dimensionality reduction)")
    create_model_state = create_model_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Train Citeseq Model===============")
    train_test = Test_Train(session_state=create_model_state)
    train_state = train_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Citeseq Cluster Analysis===============")
    cluster_analysis_test = Test_Cluster_Analysis(session_state=train_state)
    cluster_analysis_state = cluster_analysis_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")
    
    print()
    print(f"{bcolors.BOLD}===============Testing Create Solo Model===============")
    create_model_test = Test_Create_Model(session_state=pp_state, model="Solo (doublet removal)")
    create_model_state = create_model_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Train solo Model===============")
    train_test = Test_Train(session_state=create_model_state)
    train_state = train_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Solo Cluster Analysis===============")
    cluster_analysis_test = Test_Cluster_Analysis(session_state=train_state)
    cluster_analysis_state = cluster_analysis_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")
    
    print()
    print(f"{bcolors.BOLD}===============Testing Create DeepST Model===============")
    create_model_test = Test_Create_Model(session_state=pp_state, model="DeepST (identify spatial domains)")
    create_model_state = create_model_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Train DeepST Model===============")
    train_test = Test_Train(session_state=create_model_state)
    train_state = train_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing DeepST Cluster Analysis===============")
    cluster_analysis_test = Test_Cluster_Analysis(session_state=train_state)
    cluster_analysis_state = cluster_analysis_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")
    
    print()
    print(f"{bcolors.BOLD}===============Testing Upload paul15===============")
    upload_test = Test_Upload(session_state=dashboard_state, dataset="paul15")
    upload_state = upload_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Trajectory Inference===============")
    trajectory_inference_test = Test_Trajectory_Inference(session_state=upload_state)
    trajectory_inference_state = trajectory_inference_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")
    
    print()
    print(f"{bcolors.BOLD}===============Testing Upload merfish===============")
    upload_test = Test_Upload(session_state=dashboard_state, dataset="merfish")
    upload_state = upload_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")

    print()
    print(f"{bcolors.BOLD}===============Testing Spatial Transcriptomics===============")
    spatial_transcriptomics_test = Test_Spatial_Transcriptomics(session_state=upload_state)
    spatial_transcriptomics_state = spatial_transcriptomics_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")
    
    print()
    print(f"{bcolors.BOLD}===============Test Terminal===============")
    terminal_test = Test_Terminal(session_state=spatial_transcriptomics_state)
    terminal_state = terminal_test.get_final_session_state()
    print()
    print(f"{bcolors.OKGREEN}TEST PASSED{bcolors.ENDC}")
    
    print()
    print("----------------------------------------------")
    print(f"Tests completed: {date.today().strftime('%B %d, %Y')} at {datetime.now().strftime('%H:%M:%S')}\n")
    print(f"{bcolors.BOLD}ALL TESTS SUCCESSFUL.{bcolors.ENDC}")
    print()
    print(f"Removing test data...{bcolors.ENDC}")

except Exception as e:
    print()
    print(f"{bcolors.FAIL}TEST FAILED{bcolors.ENDC}")
    print(e)

finally:

    #tear down

    #remove test records from db
    workspace_name = f"workspace_name_{nonce}"
    conn.query(schemas.Workspaces).filter(schemas.Workspaces.workspace_name == workspace_name).delete()
    conn.commit()

    #remove files
    workspace_dir = os.getenv('WORKDIR')
    shutil.rmtree(workspace_dir, ignore_errors=True)
    
    print()
    print(f"{bcolors.BOLD}Tests Complete!{bcolors.ENDC}")
    print("----------------------------------------------")



