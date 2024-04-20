def get_full_image_url(request, image):
    current_domain = request.build_absolute_uri('/')[:-1]
    return f'{current_domain}/media/{image}'
