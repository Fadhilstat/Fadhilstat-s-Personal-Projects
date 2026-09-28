#!/usr/bin/env python3
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


ROUTE = "RENDER_NATIVE"
SOURCE_PLANE = "GITHUB_NATIVE"
EXPECTED_BRANCH = "canary/disjoint-render-v1251"
SOURCE_SHA = os.environ.get("CANARY_SOURCE_SHA", "UNSET")
CANARY_VERSION = "v1251"


def payload():
    seed = f"{ROUTE}|{SOURCE_PLANE}|{EXPECTED_BRANCH}|{SOURCE_SHA}|{CANARY_VERSION}"
    return {
        "status": "PASS",
        "canary_version": CANARY_VERSION,
        "route": ROUTE,
        "source_plane": SOURCE_PLANE,
        "source_branch": EXPECTED_BRANCH,
        "source_sha": SOURCE_SHA,
        "evidence_sha256": hashlib.sha256(seed.encode("utf-8")).hexdigest(),
        "vps_route_runtime": False,
        "rdc_required": False,
        "production_mutation": False,
        "database_mutation": False,
        "credential_copy": False,
        "public_control_repo": False,
        "failure_domains": ["github", "render"],
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_GET(self):
        if self.path not in {"/", "/health", "/canary"}:
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps(payload(), sort_keys=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
