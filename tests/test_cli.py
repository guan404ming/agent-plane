import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from skills import run_project

class TestDryRun(unittest.TestCase):
    @patch("skills.subprocess.run")
    @patch("skills.shutil.copy")
    @patch("skills.print")
    def test_dry_run_no_execution(self, mock_print, mock_copy, mock_run):
        # Setup mock config
        mock_config = {
            "name": "test-project",
            "path": ".",
            "enabled": True,
            "provider": "claude",
            "_dir": Path("skills/example") # Ensure this path exists or mock it
        }

        # Run with dry_run=True
        run_project(mock_config, dry_run=True)

        # Verify copy and run were NOT called
        mock_copy.assert_not_called()
        mock_run.assert_not_called()
        
        # Verify output indicates dry run
        args, _ = mock_print.call_args_list[0]
        self.assertIn("[DRY RUN]", args[0])

if __name__ == "__main__":
    unittest.main()
