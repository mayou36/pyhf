import logging
log = logging.getLogger(__name__)

from . import modifier
from .. import get_backend

@modifier(name='normsys', constrained=True, shared=True)
class normsys(object):
    def __init__(self, nom_data, modifier_data):
        self.n_parameters = 1
        self.suggested_init = [0.0]
        self.suggested_bounds = [[-5, 5]]

        self.at_zero = 1
        self.at_minus_one = {}
        self.at_plus_one = {}
        self.auxdata = [0]  # observed data is always at a = 1

    def add_sample(self, channel, sample, modifier_def):
        log.info('Adding sample {0:s} to channel {1:s}'.format(sample['name'], channel['name']))
        self.at_minus_one.setdefault(channel['name'], {})[sample['name']] = modifier_def['data']['lo']
        self.at_plus_one.setdefault(channel['name'], {})[sample['name']] = modifier_def['data']['hi']

    def alphas(self, pars):
        return pars  # the nuisance parameters correspond directly to the alpha

    def expected_data(self, pars):
        return self.alphas(pars)

    def pdf(self, a, alpha):
        tensorlib, _ = get_backend()
        return tensorlib.normal(a, alpha, 1)
