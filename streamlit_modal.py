#deployment into modal
import shlex
import subprocess
from pathlib import Path
import os
import seaborn as sns
#rom dotenv import load_dotenv

import modal

# Load environment variables from .env file
#load_dotenv()

streamlit_script_local_path = Path(__file__).parent / "streamlit_run.py"
streamlit_script_remote_path = "/root/streamlit_run.py"
image = (
    modal.Image.debian_slim(python_version="3.9")
    .uv_pip_install(
    "streamlit",
    "supabase",
    "pandas",
    "plotly",
    "python-dotenv",
    "matplotlib",
    "seaborn"
)
    .env({"FORCE_REBUILD": "true"})  # Add this line to force a rebuild
    .add_local_file(streamlit_script_local_path, streamlit_script_remote_path)
)
app = modal.App(name="usage-dashboard", image=image)

if not streamlit_script_local_path.exists():
    raise RuntimeError(
        "Hey your starter streamlit isnt working"
    )
##added in class, created a secret and put a password for the modal environment 
#ddit a code where i took secert and deploy it
@app.function(secrets=[modal.Secret.from_name("prem-secret")])
@modal.web_server(8000)
def run():
    target = shlex.quote(streamlit_script_remote_path)
    cmd = f"streamlit run {target} --server.port 8000 --server.enableCORS=false --server.enableXsrfProtection=false"
    # Build environment variables, filtering out None values
    env_vars = {}
    if os.getenv("SUPABASE_KEY"):
        env_vars["SUPABASE_KEY"] = os.getenv("SUPABASE_KEY")
    if os.getenv("SUPABASE_URL"):
        env_vars["SUPABASE_URL"] = os.getenv("SUPABASE_URL")
    
    # Include current environment to ensure PATH and other essential vars are available
    env_vars.update(os.environ)
        
    subprocess.Popen(cmd, shell=True, env=env_vars)
    
    #in CHAT: in streamlit  can you do a supabase client that uses the keys to write out this table for. 
    
    #url to copy https://cnxqpvsljidbzvmyubeu.supabase.co
    #secret: prem-secret