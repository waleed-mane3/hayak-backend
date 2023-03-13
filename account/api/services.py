
from auth_system.models import CustomUser
from .queries import getCustomUser
class AccountService:

    @staticmethod
    def validateChildAccountFromEvents(id: int, user:CustomUser) -> bool:
        instance = getCustomUser(pk=id)


