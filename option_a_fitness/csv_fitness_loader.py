import csv
import re
from pathlib import Path


PARTICIPANT_HEADER = [
    "participant_id",
    "name",
    "baseline_heart_rate",
    "baseline_skin_response",
    "baseline_temperature",
]

SESSION_HEADER = [
    "session_id",
    "participant_id",
    "timestamp",
    "heart_rate",
    "skin_response",
    "temperature",
    "activity_level",
    "signal_quality",
]


def _is_valid_participant_id(value):
    return isinstance(value, str) and bool(re.fullmatch(r"P\d{3}", value))


def _is_valid_session_id(value):
    return isinstance(value, str) and bool(re.fullmatch(r"FIT-\d{4}-\d{3}", value))


def _parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def load_participants_from_csv(path):
    """Load valid participant rows from a CSV file and return them as dicts."""
    participants = []
    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row is None:
                continue
            clean = {key: (value.strip() if isinstance(value, str) else value) for key, value in row.items() if key is not None}
            if not clean:
                continue

            errors = []
            participant_id = clean.get("participant_id")
            if not _is_valid_participant_id(participant_id):
                errors.append("participant_id")

            baseline_heart_rate = _parse_int(clean.get("baseline_heart_rate"))
            if baseline_heart_rate is None:
                errors.append("baseline_heart_rate")

            baseline_skin_response = _parse_float(clean.get("baseline_skin_response"))
            if baseline_skin_response is None:
                errors.append("baseline_skin_response")

            baseline_temperature = _parse_float(clean.get("baseline_temperature"))
            if baseline_temperature is None:
                errors.append("baseline_temperature")

            if errors:
                continue

            participants.append({
                "participant_id": participant_id,
                "name": clean.get("name", "").strip(),
                "baseline_heart_rate": baseline_heart_rate,
                "baseline_skin_response": baseline_skin_response,
                "baseline_temperature": baseline_temperature,
            })
    return participants


def load_sessions_from_csv(path, valid_participants=None):
    """Load valid and invalid session rows from a CSV file.

    Returns a tuple: (valid_rows, invalid_rows)
    Each invalid row includes a 'reason' field for the validation problem(s).
    """
    valid_rows = []
    invalid_rows = []

    if valid_participants is None:
        valid_participants = set()
    else:
        valid_participants = set(valid_participants)

    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row is None:
                continue
            clean = {key: (value.strip() if isinstance(value, str) else value) for key, value in row.items() if key is not None}
            if not clean:
                continue

            row_errors = []
            session_id = clean.get("session_id")
            if not _is_valid_session_id(session_id):
                row_errors.append("session_id")

            participant_id = clean.get("participant_id")
            if not _is_valid_participant_id(participant_id):
                row_errors.append("participant_id")
            elif valid_participants and participant_id not in valid_participants:
                row_errors.append("unknown participant_id")

            timestamp = _parse_int(clean.get("timestamp"))
            if timestamp is None or timestamp < 0:
                row_errors.append("timestamp")

            heart_rate = _parse_float(clean.get("heart_rate"))
            if heart_rate is None or not (35 <= heart_rate <= 205):
                row_errors.append("heart_rate")

            skin_response = _parse_float(clean.get("skin_response"))
            if skin_response is None or skin_response < 0:
                row_errors.append("skin_response")

            temperature = _parse_float(clean.get("temperature"))
            if temperature is None or not (25 <= temperature <= 42):
                row_errors.append("temperature")

            activity_level = _parse_float(clean.get("activity_level"))
            if activity_level is None or not (0 <= activity_level <= 1):
                row_errors.append("activity_level")

            signal_quality = _parse_float(clean.get("signal_quality"))
            if signal_quality is None or not (0 <= signal_quality <= 1):
                row_errors.append("signal_quality")

            if row_errors:
                invalid_rows.append({
                    **clean,
                    "reason": ", ".join(row_errors),
                })
                continue

            valid_rows.append({
                "session_id": session_id,
                "participant_id": participant_id,
                "timestamp": timestamp,
                "heart_rate": heart_rate,
                "skin_response": skin_response,
                "temperature": temperature,
                "activity_level": activity_level,
                "signal_quality": signal_quality,
            })

    return valid_rows, invalid_rows


def load_fitness_data_from_csv(participants_csv_path, sessions_csv_path):
    """Convenience loader for the assignment data.

    Returns: (participants, valid_sessions, invalid_sessions)
    """
    participants = load_participants_from_csv(participants_csv_path)
    valid_ids = {p["participant_id"] for p in participants}
    valid_sessions, invalid_sessions = load_sessions_from_csv(sessions_csv_path, valid_ids)
    return participants, valid_sessions, invalid_sessions
