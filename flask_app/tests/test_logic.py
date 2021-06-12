from unittest import TestCase
from app.models import ModelCamp


class Test(TestCase):
    def test_prepare_data_for_index_configuration(self):
        self.model = ModelCamp.query.all()
        for i in self.model:
            u = i.name
            assert u == "Veles"





