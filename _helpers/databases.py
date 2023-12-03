import os
import pandas as pd


def get_from_db(path: str, index_name: str) -> pd.DataFrame:
    dataf = pd.read_csv(path, index_col=index_name)
    return dataf


def generate_folder(path: str) -> None:
    """
    Python prog to check if directory exists and creates it
    """
    # path = path_name + f'\{directory_name}'
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        print(f"The new directory is created for {path}.")
