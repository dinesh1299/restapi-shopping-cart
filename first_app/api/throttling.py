from rest_framework.throttling import UserRateThrottle


class RatingListThrottler(UserRateThrottle):
    scope = 'rating-list'

class RatingDetailThrottler(UserRateThrottle):
    scope = 'rating-detail'