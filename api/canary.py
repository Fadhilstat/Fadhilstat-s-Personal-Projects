import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler


ROUTE = "VERCEL_NATIVE"
SOURCE_PLANE = "GITHUB_NATIVE"
SOURCE_BRANCH = "canary/disjoint-render-v1251"
CANARY_VERSION = "v1251"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        source_sha = os.environ.get("VERCEL_GIT_COMMIT_SHA", "UNSET")
        seed = "|".join([
            ROUTE,
            SOURCE_PLANE,
            SOURCE_BRANCH,
            source_sha,
            CANARY_VERSION,
        ])
        payload = {
            "status": "PASS",
            "canary_version": CANARY_VERSION,
            "route": ROUTE,
            "source_plane": SOURCE_PLANE,
            "source_branch": SOURCE_BRANCH,
            "source_sha": source_sha,
            "evidence_sha256": hashlib.sha256(
                seed.encode("utf-8")
            ).hexdigest(),
            "vps_route_runtime": False,
            "rdc_required": False,
            "production_mutation": False,
            "database_mutation": False,
            "credential_copy": False,
            "failure_domains": ["github", "vercel"],
        }
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
