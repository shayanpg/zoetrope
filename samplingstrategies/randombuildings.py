from .strategy import SamplingStrategy

from neighborhood.models import Neighborhood
from accounts.models import Profile

class RandomBuildings(SamplingStrategy):
    NAME = 'Random Buildings'

    CONFIG = {
        'name':[str, NAME],
        'num_points': [int, "Number of points to sample"],
        'neighborhood': [Neighborhood, "Neighborhood model to sample"],
        'tolerance': [int, "How many retries should be allowed for points without image results"],
        'user': [Profile, "Representation of the calling User"],
        }
    CONFIG = {**(SamplingStrategy.CONFIG), **CONFIG} # Include entries from SamplingStrategy, **CONFIG is second arg to override super()

    def sample(self, request): # request is JSON with same keys as config, with values being actual value instances
        pass
    
    def orient_images(self):
        pass

    def snap_points(self):
        pass
