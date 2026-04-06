from .adapters import DiscordAdapter, GoogleAdapter
from .models import CustomUser
from .utils import decode_jwt_without_verification


class OAuthFacade:

    def authenticate(self, token, provider):

        payload = decode_jwt_without_verification(token)

        if provider == "discord":
            adapter = DiscordAdapter()
        elif provider == "google":
            adapter = GoogleAdapter()
        else:
            raise Exception("Unsupported provider")

        user_data = adapter.get_user_data(payload)

        email = user_data["email"]
        name = user_data["name"]

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "username": email.split("@")[0],
                "name": name,
                "role": "resident",
            },
        )

        return user
