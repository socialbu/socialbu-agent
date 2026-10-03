#!/usr/bin/env python3
"""Check that releases cannot skip a missing or misconfigured Claude endpoint."""

import unittest
import urllib.error
from unittest.mock import patch

import validate


class LiveEndpointTest(unittest.TestCase):
    def check_endpoints(self, claude_status=401, claude_metadata="/mcp/claude"):
        visited = []

        def respond(request, timeout):
            visited.append(request.full_url)
            claude = request.full_url.endswith("/claude")
            metadata = claude_metadata if claude else ""
            raise urllib.error.HTTPError(
                request.full_url,
                claude_status if claude else 401,
                "Unauthorized",
                {"WWW-Authenticate": f'Bearer resource_metadata="https://socialbu.com/.well-known/oauth-protected-resource{metadata}"'},
                None,
            )

        with patch("urllib.request.urlopen", side_effect=respond):
            validate.validate_live_endpoint()
        return visited

    def test_checks_both_endpoints(self):
        self.assertEqual([validate.MCP_URL, f"{validate.MCP_URL}/claude"], self.check_endpoints())

    def test_missing_claude_endpoint_blocks_release(self):
        with self.assertRaises(AssertionError):
            self.check_endpoints(claude_status=404)

    def test_generic_oauth_challenge_cannot_stand_in_for_claude(self):
        with self.assertRaises(AssertionError):
            self.check_endpoints(claude_metadata="")


if __name__ == "__main__":
    unittest.main()
