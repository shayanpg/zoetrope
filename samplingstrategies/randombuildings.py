from .strategy import SamplingStrategy

class RandomBuildings(SamplingStrategy):
    NAME = 'Random Buildings'

    CONFIG = {'name':[str, NAME]}
    CONFIG = {**(SamplingStrategy.CONFIG), **CONFIG} # Include entries from SamplingStrategy, **CONFIG is second arg to override super()

    def sample(self, request): # request is JSON with same keys as config, with values being actual value instances
        pass
    
    def orient_images(self):
        pass

    def snap_points(self):
        pass
