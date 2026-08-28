import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import authz
import platform_check
import tools


class AuthorizationGuardrailTests(unittest.TestCase):
    def test_rejects_urls_paths_and_shell_fragments(self):
        bad_targets = [
            "https://example.com",
            "example.com/admin",
            "example.com;whoami",
            "-oG",
            "example.com && curl localhost",
        ]
        for target in bad_targets:
            with self.subTest(target=target):
                with self.assertRaises(authz.ScopeError):
                    authz.validate_target_format(target)

    def test_private_and_local_targets_are_allowed_without_scope_file_entries(self):
        for target in ["localhost", "127.0.0.1", "192.168.1.10", "10.0.0.0/24", "printer.local"]:
            with self.subTest(target=target):
                self.assertTrue(authz.is_in_scope(target, {"authorized": [], "excluded": []}))

    def test_public_targets_require_explicit_authorized_scope(self):
        scope = {"authorized": ["example.com", "203.0.113.0/24"], "excluded": []}
        self.assertTrue(authz.is_in_scope("www.example.com", scope))
        self.assertTrue(authz.is_in_scope("203.0.113.42", scope))
        self.assertFalse(authz.is_in_scope("unauthorized.example", {"authorized": [], "excluded": []}))

    def test_scope_file_is_created_with_private_permissions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            scope_path = Path(tmpdir) / "scope.json"
            with patch.object(authz, "SCOPE_FILE", scope_path):
                self.assertEqual(authz.scope_path(), scope_path)
                mode = scope_path.stat().st_mode & 0o777
                self.assertEqual(mode, 0o600)

    def test_llm_tool_dispatch_blocks_out_of_scope_public_targets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            scope_path = Path(tmpdir) / "scope.json"
            with patch.object(authz, "SCOPE_FILE", scope_path), patch.object(tools, "run_tool") as run_tool:
                result = tools.run_tool_by_command("nmap -sV example.com")
        self.assertIn("Blocked target for nmap", result)
        run_tool.assert_not_called()

    def test_llm_tool_dispatch_runs_authorized_or_local_targets_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            scope_path = Path(tmpdir) / "scope.json"
            with patch.object(authz, "SCOPE_FILE", scope_path), patch.object(tools, "run_tool", return_value="ok") as run_tool:
                local_result = tools.run_tool_by_command("nmap -sV localhost")
                authz.add_scope_entry("example.com")
                public_result = tools.run_tool_by_command("dig A example.com")
        self.assertEqual(local_result, "ok")
        self.assertEqual(public_result, "ok")
        run_tool.assert_any_call(["nmap", "-sV", "localhost"])
        run_tool.assert_any_call(["dig", "A", "example.com"])

    def test_nikto_h_target_is_authorized_before_execution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            scope_path = Path(tmpdir) / "scope.json"
            with (
                patch.object(authz, "SCOPE_FILE", scope_path),
                patch.object(tools, "run_tool", return_value="ok") as run_tool,
            ):
                blocked_result = tools.run_tool_by_command("nikto -h example.com -nointeractive")
                local_result = tools.run_tool_by_command("nikto -h localhost -nointeractive")
        self.assertIn("Blocked target for nikto", blocked_result)
        self.assertEqual(local_result, "ok")
        run_tool.assert_called_once_with(["nikto", "-h", "localhost", "-nointeractive"])


class PlatformDoctorTests(unittest.TestCase):
    def test_ollama_defaults_to_local_endpoint(self):
        with patch.dict(os.environ, {}, clear=True):
            status = platform_check.ollama_status()
        self.assertEqual(status["url"], "http://localhost:11434/api/generate")
        self.assertTrue(status["local"])

    def test_remote_ollama_endpoint_is_reported_as_non_local(self):
        status = platform_check.ollama_status(url="https://ollama.example.com/api/generate")
        self.assertFalse(status["local"])

    def test_doctor_report_includes_required_and_optional_tools(self):
        report_names = {name for name, _state, _detail in platform_check.doctor_report(db_path=__file__)}
        self.assertIn("SQLite database", report_names)
        for tool in platform_check.REQUIRED_TOOLS + platform_check.OPTIONAL_TOOLS:
            self.assertIn(tool, report_names)


if __name__ == "__main__":
    unittest.main()
