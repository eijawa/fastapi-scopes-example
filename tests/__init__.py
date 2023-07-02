# ========
# Весь блок кода ниже нужен только для того,
# чтобы миграции адекватно работали при разработке
import os
from dotenv import load_dotenv, find_dotenv
env_path = find_dotenv(
    os.getenv("ENV_FILE", "configs/develop.env"), raise_error_if_not_found=True
)
load_dotenv(env_path)
# ========
