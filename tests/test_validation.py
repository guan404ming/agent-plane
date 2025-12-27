import unittest
from pathlib import Path
from skills import validate_project

class TestValidation(unittest.TestCase):
    def test_missing_fields(self):
        config = {}
        errors = validate_project(config)
        self.assertIn("Missing 'name'", errors)
        self.assertIn("Missing 'path'", errors)

    def test_invalid_path(self):
        config = {
            "name": "test",
            "path": "/non/existent/path",
            "provider": "claude"
        }
        errors = validate_project(config)
        # We expect error about target path
        self.assertTrue(any("Target path not found" in e for e in errors))

    def test_invalid_provider(self):
        config = {
            "name": "test",
            "path": ".",
            "provider": "unknown"
        }
        errors = validate_project(config)
        self.assertTrue(any("Invalid provider" in e for e in errors))

    def test_valid_config(self):
        # We need a directory that has .md files. skills/example is good candidate.
        # But we need to resolve the path relative to where test runs.
        # Assuming we run from root.
        example_dir = Path("skills/example")
        if not example_dir.exists():
            self.skipTest("skills/example not found")

        config = {
            "name": "example",
            "path": ".",
            "provider": "gemini",
            "_dir": example_dir
        }
        errors = validate_project(config)
        self.assertEqual(errors, [], f"Expected no errors, got {errors}")

if __name__ == '__main__':
    unittest.main()
