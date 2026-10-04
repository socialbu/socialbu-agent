#!/usr/bin/env python3
"""Check reachability and shared OAuth discovery for the hosted connection."""

import unittest
import urllib.error
from unittest.mock import patch

import validate


class LiveEndpointTest(unittest.TestCase):
    def check_endpoint(self, status=401, metadata="https://socialbu.com/.well-known/oauth-protected-resource"):
        visited = []

        def respond(request, timeout):
            self.assertEqual("SocialBu-Agent-Validation/1.0", request.get_header("User-agent"))
            visited.append(request.full_url)
            raise urllib.error.HTTPError(
                request.full_url,
                status,
                "Unauthorized",
                {"WWW-Authenticate": f'Bearer resource_metadata="{metadata}"'},
                None,
            )

        with patch("urllib.request.urlopen", side_effect=respond):
            validate.validate_live_endpoint()
        return visited

    def test_checks_the_shared_endpoint(self):
        self.assertEqual([validate.MCP_URL], self.check_endpoint())

    def test_missing_endpoint_blocks_release(self):
        with self.assertRaises(AssertionError):
            self.check_endpoint(status=404)

    def test_wrong_discovery_origin_blocks_release(self):
        with self.assertRaises(AssertionError):
            self.check_endpoint(metadata="https://staging.example/.well-known/oauth-protected-resource")


if __name__ == "__main__":
    unittest.main()
