"""Error mapping of the Google HTTP adapters, with httpx.MockTransport (no network)."""
import unittest

try:
    import httpx
except ImportError:  # pragma: no cover
    httpx = None


@unittest.skipIf(httpx is None, "httpx not installed")
class AdapterErrorMappingTests(unittest.TestCase):
    def _provider(self, handler):
        from support_agent.gmail_http import GoogleOAuthProvider
        return GoogleOAuthProvider("client-1", "test-secret", http=httpx.Client(transport=httpx.MockTransport(handler)))

    def test_invalid_grant_is_distinct_from_outage_and_malformed_body(self):
        from support_agent.gmail_oauth import InvalidGrant, ProviderError
        with self.assertRaises(InvalidGrant):
            self._provider(lambda r: httpx.Response(400, json={"error": "invalid_grant"})).refresh("rt")
        for resp in (httpx.Response(503), httpx.Response(429), httpx.Response(200, text="not json")):
            with self.assertRaises(ProviderError):
                self._provider(lambda r, resp=resp: resp).refresh("rt")

    def test_token_response_parses_granted_scopes(self):
        body = {"access_token": "at", "expires_in": 3599, "refresh_token": "rt",
                "scope": "openid https://www.googleapis.com/auth/gmail.readonly"}
        tokens = self._provider(lambda r: httpx.Response(200, json=body)).exchange_code("c", "v", "https://x/cb")
        self.assertIn("https://www.googleapis.com/auth/gmail.readonly", tokens.scopes)

    def test_gmail_401_is_resource_unauthorized_and_errors_hide_bodies(self):
        from support_agent.gmail_http import HttpxGmailClient
        from support_agent.gmail_tool import GmailUnavailable, ResourceUnauthorized
        client = HttpxGmailClient(http=httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(401))))
        with self.assertRaises(ResourceUnauthorized):
            client.list_message_ids("at", "q", 3)
        client = HttpxGmailClient(http=httpx.Client(transport=httpx.MockTransport(
            lambda r: httpx.Response(403, text="CANARY-BODY"))))
        with self.assertRaises(GmailUnavailable) as caught:
            client.get_message("at", "m1")
        self.assertNotIn("CANARY", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
