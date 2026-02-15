class BaseOAuthAdapter:
    """Abstract adapter"""
    def get_user_data(self, payload):
        raise NotImplementedError("Subclasses must implement this method")


class DiscordAdapter(BaseOAuthAdapter):
    def get_user_data(self, payload):
        return {
            "email": payload.get("email"),
            "name": payload.get("name") or payload.get("email"),
        }


class GoogleAdapter(BaseOAuthAdapter):
    def get_user_data(self, payload):
        return {
            "email": payload.get("email"),
            "name": payload.get("given_name") or payload.get("name"),
        }
