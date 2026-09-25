import csv
import os
import tempfile
import unittest

try:
    from .csv_fitness_loader import load_participants_from_csv, load_sessions_from_csv
except ImportError:  # pragma: no cover
    from csv_fitness_loader import load_participants_from_csv, load_sessions_from_csv


class CsvFitnessLoaderTests(unittest.TestCase):
    def test_load_participants_from_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "participants.csv")
            with open(path, "w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["participant_id", "name", "baseline_heart_rate", "baseline_skin_response", "baseline_temperature"])
                writer.writerow(["P001", "Amina Noor", "68", "1.20", "32.4"])
                writer.writerow(["P002", "Jonas Berg", "74", "1.45", "32.7"])

            participants = load_participants_from_csv(path)

            self.assertEqual(len(participants), 2)
            self.assertEqual(participants[0]["participant_id"], "P001")
            self.assertEqual(participants[1]["baseline_heart_rate"], 74)

    def test_load_sessions_from_csv_reports_invalid_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            participants_path = os.path.join(tmpdir, "participants.csv")
            sessions_path = os.path.join(tmpdir, "sessions.csv")

            with open(participants_path, "w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["participant_id", "name", "baseline_heart_rate", "baseline_skin_response", "baseline_temperature"])
                writer.writerow(["P001", "Amina Noor", "68", "1.20", "32.4"])
                writer.writerow(["P002", "Jonas Berg", "74", "1.45", "32.7"])

            with open(sessions_path, "w", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["session_id", "participant_id", "timestamp", "heart_rate", "skin_response", "temperature", "activity_level", "signal_quality"])
                writer.writerow(["FIT-2026-001", "P001", "0", "68", "1.18", "32.4", "0.08", "0.98"])
                writer.writerow(["FIT-2026-001", "P001", "1", "fast", "1.20", "32.4", "0.10", "0.97"])
                writer.writerow(["FIT-2026-002", "P999", "0", "80", "1.60", "32.8", "0.20", "0.95"])

            valid_rows, invalid_rows = load_sessions_from_csv(sessions_path, {"P001": True, "P002": True})

            self.assertEqual(len(valid_rows), 1)
            self.assertEqual(len(invalid_rows), 2)
            self.assertIn("participant_id", invalid_rows[1]["reason"])


if __name__ == "__main__":
    unittest.main()
