# Smart Fitness Session Analyzer

This project reads fitness session data, validates each reading, and classifies a session as resting, moderate activity, high activity, recovery, or poor quality.

## Project structure

- `option_a_fitness/fitness_analyzer.py` contains the participant model, observation validation, and classification logic.
- `option_a_fitness/csv_fitness_loader.py` loads participant and session records from CSV files.
- `sample_data.py` generates sample fitness sessions for testing and demo runs.
- `data/option_a_fitness/` contains the CSV datasets used by the assignment.

## Run the application

```bash
python3 main.py
```

## Run the tests

```bash
python3 -m unittest -v
```

## Example: generate and analyze 50 sample sessions

```bash
python3 -c "from sample_data import generate_fitness_data; from option_a_fitness.fitness_analyzer import FitnessSessionAnalyzer; results=[]; 
for i in range(50):
    profile, observations = generate_fitness_data(participant_id=f'P{i:03d}', scenario='random', seed=i, number_of_windows=12)
    analyzer = FitnessSessionAnalyzer(profile, observations)
    results.append({'participant_id': profile['participant_id'], 'classification': analyzer.session_summary['classification'], 'valid_observations': analyzer.session_summary['valid_observations'], 'rejected_observations': analyzer.session_summary['rejected_observations']})
print(f'Analyzed {len(results)} sessions'); print(results[:5])"
```

This is useful for creating a larger sample batch and checking how the classifier behaves across many generated sessions.

## Example: load the CSV data

```bash
python3 -c "from option_a_fitness.csv_fitness_loader import load_fitness_data_from_csv; participants, valid_sessions, invalid_sessions = load_fitness_data_from_csv('data/option_a_fitness/participants.csv', 'data/option_a_fitness/fitness_sessions.csv'); print(len(participants), len(valid_sessions), len(invalid_sessions))"
```

## Notes

- The project uses only the Python standard library.
- There are no third-party dependencies required for this assignment.

