
def get_current_domain(self):
    return self.request.build_absolute_uri('/')[:-1]


def get_thumbnail_url(self, thumbnail):
    if 'https' in str(thumbnail):
        return f'{thumbnail}'
    else:
        return f'{get_current_domain(self)}/media/{thumbnail}'
