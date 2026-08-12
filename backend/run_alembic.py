import subprocess
import os

os.chdir(r"c:\Users\praveen v\Desktop\Evalynx\backend")
env = os.environ.copy()

result = subprocess.run([r"venv\Scripts\python", "-m", "alembic", "revision", "--autogenerate", "-m", "add_proctoring_fields"], env=env, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("ERR:", result.stderr)
