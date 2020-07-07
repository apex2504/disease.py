class APIError(Exception):
    pass

class NotFound(Exception):
    pass

class BadSortParameter(Exception):
    pass

class BadYesterdayParameter(Exception):
    pass

class BadTwoDaysAgoParameter(Exception):
    pass

class BadAllowNoneParameter(Exception):
    pass