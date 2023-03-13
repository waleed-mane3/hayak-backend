
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from enum import Enum
import logging
logger = logging.getLogger('django')


class Error(Enum):
    DEFAULT_ERROR = {'code': -2323, 'detail': _('Something went wrong!')}
    INVALID_JWT_TOKEN = {'code': -100, 'detail': _('Invalid token!')}
    INSTANCE_NOT_FOUND = {'code': -404, 'detail': _('{} not found!')}
    REQUIRED_FIELD = {'code': 0, 'detail': _('This field is required!')}
    DATA_IS_MISSING = {'code': -101, 'detail': _('{} Data is missing!')}
    NO_ACTIVE_ACCOUNT = {'code': -500, 'detail': _('No active account found with the given credentials!')}
    PASSWORD = {'code': -500, 'detail': _('Password {}')}
    FEILD_IS_REQUIRED = {'code': -400, "detail": _('{}: This field is required.')}




class APIError:
    def __init__(self, error: Error, extra=None):
        self.error = error
        self.extra = extra or None
        error_detail = error.value
        if self.extra:
            # Extra values can be used in foramtting a string that contains {}
            if isinstance(self.extra, list):
                error_detail['detail'] = error_detail['detail'].format(*extra)
        try:
            logger.info(error.value)
        except BaseException:
            pass
        raise ValidationError(**error_detail)
