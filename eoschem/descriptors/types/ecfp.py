from . import BaseDescriptorType
import numpy as np
from rdkit.Chem import rdMolDescriptors as rd

radius = 3
nBits = 2048
<<<<<<< HEAD


def clip(v):
    if v > 255:
        v = 255
    return v
=======
>>>>>>> 8a05dcf7bcbfbee32aa23019194890e2b9ee485e


def clip(v):
    if v > 255:
        v = 255
    return v


class Ecfp(BaseDescriptorType):

    def __init__(self):
        super().__init__()
        self.radius = radius
        self.nbits = nBits

<<<<<<< HEAD
=======
<<<<<<< HEAD
    def _calc(self, mols):
        fps = [
            AllChem.GetMorganFingerprint(
                mol, self.radius, useCounts=self.useCounts,
                useFeatures=self.useFeatures)
            for mol in mols
        ]
        size = 2048
        nfp = np.zeros((len(fps), size), np.int32)
        for i, fp in enumerate(fps):
            for idx, v in fp.GetNonzeroElements().items():
                nidx = idx % size
                nfp[i, nidx] += int(v)
        return np.array(nfp, dtype=np.int32)
=======
>>>>>>> 8a05dcf7bcbfbee32aa23019194890e2b9ee485e
    def calc(self, mols):
        fingerprints = []
        for mol in mols:
            counts = list(rd.GetHashedMorganFingerprint(mol, radius=self.radius, nBits=self.nbits))
            counts = [clip(x) for x in counts]
            fingerprints += [counts]
        return np.array(fingerprints)
<<<<<<< HEAD
=======
>>>>>>> f7356c4... Major updates
>>>>>>> 8a05dcf7bcbfbee32aa23019194890e2b9ee485e
