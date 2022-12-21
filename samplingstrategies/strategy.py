class SamplingStrategy:
    name = 'DEFAULT'
    parameters_taken = []

    def __str__(self):
        return self.name

    def sample(polygon_points, *args, **kwargs):
        return []

    def orient_images(*args, **kwargs):
        return

    def snap_points(*args, **kwargs):
        return