from django.contrib import messages

from gsv import settings
from utils import str_to_dic, sample_from_area, download_images, reverse_geocode, MONTH_MAP

from .strategy import SamplingStrategy

from neighborhood.models import Neighborhood
from address.models import Address
from pull.models import Pull
from accounts.models import Profile

class RandomBuildings(SamplingStrategy):
    NAME = 'Random Buildings'

    CONFIG = {
        'name':[str, NAME],
        'num_points': [int, "Number of points to sample"],
        'neighborhood': [Neighborhood, "Neighborhood model to sample"],
        'tolerance': [int, "How many retries should be allowed for points without image results"],
        'user': [Profile, "Representation of the calling User"],
        'pull': [Pull, "Pull for calling request"],
        'sample_list': [list, "List in which to put sampled points"],
        'message_q': [list, "List in which to put messages for display on results page. Format [messages.TYPE, 'message string']"],
        }
    CONFIG = {**(SamplingStrategy.CONFIG), **CONFIG} # Include entries from SamplingStrategy, **CONFIG is second arg to override super()

    def orient_images(self):
        pass

    def snap_points(self):
        pass

    def valid_address(self, address):
        valid = (
            address
            and '+' not in address
        )
        return valid

    def sample(self, request): # request is JSON with same keys as config, with values being actual value instances
        num_points = request.get('num_points')
        tolerance = request.get('tolerance')
        n = request.get('neighborhood')
        pts = str_to_dic(n.points)
        user = request.get('user')
        pull = request.get('pull')
        
        sample = request.get('sample_list')
        message_q = request.get('message_q')

        num_sampled = 0 # Number of successfully downloaded points
        num_attempts = 0
        max_attempts = num_points + tolerance
        while num_sampled < num_points and num_attempts < max_attempts:
            num_attempts += 1
            p = sample_from_area(pts, 1)[0]
            # CREATE ADDRESS w/ reverse_geocode
            address = reverse_geocode(p['lat'], p['lng'], settings.MAPS_API_KEY)
            user.dec_remaining_calls(1)
            if not self.valid_address(address):
                print("Invalid address")
                continue
            a = Address(name=address, lat=str(p['lat']), lng=str(p['lng']))
            a.save()
            a.neighborhoods.add(n)
            print("Address:", address)
            fname = address.replace(' ', '_').replace(',', '')
            print('p:', p)
            try:
                dates, urls = download_images(p['lat'], p['lng'], settings.GSV_API_KEY, pull, a, fname)
            except TypeError:
                print("Download images failed for", address)
                continue
            assert len(dates) == len(urls)
            if not urls:
                message_q.append([messages.WARNING, f'No Photos Found for "{address}".'])
            else:
                num_sampled += 1
                sample.append(p)
                for i in range(len(urls)):
                    year, month = dates[i][0], dates[i][1]
                    message = address +" in " + MONTH_MAP[int(month)] + ", " + str(year)
                    message_q.append([messages.INFO, message])
                    message_q.append([messages.INFO, urls[i]])
                user.dec_remaining_calls(len(urls))
        print("num sampled:", num_sampled)
        print("num attempts:", num_attempts)
