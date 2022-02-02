# Version
__version__ = "0.0.1"

# Disable third-party warnings
import warnings

warnings.filterwarnings("ignore")

try:
    from rdkit import RDLogger

    RDLogger.DisableLog("rdApp.*")
except:
    pass

# Internal imports
from .utils.logging import logger

# Base Zaira class
import json
import os
import numpy as np
import pandas as pd
from time import time
from .vars import BASE_DIR, DATA_FILENAME, DATA_SUBFOLDER
from .vars import SESSION_FILE
from .vars import ENSEMBLE_MODE


class ZairaBase(object):
    def __init__(self):
        self.logger = logger

    def get_output_dir(self):
        with open(os.path.join(BASE_DIR, SESSION_FILE), "r") as f:
            session = json.load(f)
        return session["output_dir"]

    def get_elapsed_time(self):
        with open(os.path.join(BASE_DIR, SESSION_FILE), "r") as f:
            session = json.load(f)
        return session["elapsed_time"]

    def reset_time(self):
        with open(os.path.join(BASE_DIR, SESSION_FILE), "r") as f:
            session = json.load(f)
        session["time_stamp"] = int(time())
        with open(os.path.join(BASE_DIR, SESSION_FILE), "w") as f:
            json.dump(session, f, indent=4)

    def update_elapsed_time(self):
        with open(os.path.join(BASE_DIR, SESSION_FILE), "r") as f:
            session = json.load(f)
        delta_time = int(time()) - session["time_stamp"]
        session["elapsed_time"] = session["elapsed_time"] + delta_time
        with open(os.path.join(BASE_DIR, SESSION_FILE), "w") as f:
            json.dump(session, f, indent=4)

    def get_trained_dir(self):
        with open(os.path.join(BASE_DIR, SESSION_FILE), "r") as f:
            session = json.load(f)
        return session["model_dir"]

    def is_predict(self):
        trained_dir = self.get_trained_dir()
        if os.path.exists(trained_dir):
            return True
        else:
            return False

    def is_train(self):
        if self.is_predict():
            return False
        else:
            return True

    def _dummy_indices(self, path):
        df = pd.read_csv(os.path.join(path, DATA_SUBFOLDER, DATA_FILENAME))
        idxs = np.array([i for i in range(df.shape[0])])
        return idxs

    def get_train_indices(self, path):
        if ENSEMBLE_MODE == "blending":
            self.logger.debug("Getting a training set")
            fold = np.array(
                pd.read_csv(os.path.join(path, DATA_SUBFOLDER, DATA_FILENAME))[
                    "fld_val"
                ]
            )
            idxs = np.array([i for i in range(len(fold))])
            idxs = idxs[fold == 0]
            return idxs
        else:
            self.logger.debug(
                "Training set is the full dataset. Interpret with caution!"
            )
            idxs = self._dummy_indices(path)
            return idxs

    def get_validation_indices(self, path):
        if ENSEMBLE_MODE == "blending":
            self.logger.debug("Getting a validation set")
            fold = np.array(
                pd.read_csv(os.path.join(path, DATA_SUBFOLDER, DATA_FILENAME))[
                    "fld_val"
                ]
            )
            idxs = np.array([i for i in range(len(fold))])
            idxs = idxs[fold == 1]
            return idxs
        else:
            self.logger.debug(
                "Validation set is equivalent to the training set. Interpret with caution!"
            )
            idxs = self._dummy_indices(path)
            return idxs


__all__ = ["__version__"]
