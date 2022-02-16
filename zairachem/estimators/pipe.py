from .. import ZairaBase
from .from_individual_full_descriptors.pipe import IndividualFullDescriptorPipeline
from .from_manifolds.pipe import ManifoldPipeline
from .from_reference_embedding.pipe import ReferenceEmbeddingPipeline
from .from_molmap.pipe import MolMapPipeline
from .evaluate import SimpleEvaluator


class EstimatorPipeline(ZairaBase):
    def __init__(self, path):
        ZairaBase.__init__(self)
        if path is None:
            self.path = self.get_output_dir()
        else:
            self.path = path

    def _individual_estimator_pipeline(self, time_budget_sec):
        self.logger.debug("Running individual estimator pipeline")
        p = IndividualFullDescriptorPipeline(path=self.path)
        p.run(time_budget_sec=time_budget_sec)

    def _manifolds_pipeline(self, time_budget_sec):
        self.logger.debug("Running manifolds estimator pipeline")
        p = ManifoldPipeline(path=self.path)
        p.run(time_budget_sec=time_budget_sec)

    def _reference_pipeline(self, time_budget_sec):
        self.logger.debug("Reference embedding pipeline")
        p = ReferenceEmbeddingPipeline(path=self.path)
        p.run(time_budget_sec=time_budget_sec)

    def _molmap_pipeline(self, time_budget_sec):
        self.logger.debug("Molmap estimator pipeline")
        p = MolMapPipeline(path=self.path)
        p.run(time_budget_sec=time_budget_sec)

    def _simple_evaluation(self):
        SimpleEvaluator(path=self.path).run()

    def run(self, time_budget_sec=None):
        #self._individual_estimator_pipeline(time_budget_sec)
        #self._manifolds_pipeline(time_budget_sec)
        #self._reference_pipeline(time_budget_sec)
        self._molmap_pipeline(time_budget_sec)
        self._simple_evaluation()
