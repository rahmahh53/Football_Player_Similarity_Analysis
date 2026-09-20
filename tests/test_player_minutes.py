from src.features.player_minutes import calculate_player_minutes


def test_full_match_minutes():
    positions = [{"from": "00:00", "to": None}]
    minutes = calculate_player_minutes(positions=positions, match_end_time="90:00")
    assert minutes == 90


def test_substitute_minutes():
    positions = [{"from": "60:00", "to": None}]
    minutes = calculate_player_minutes(positions=positions, match_end_time="95:00")
    assert minutes == 35


def test_overlapping_intervals_are_not_double_counted():
    positions = [
        {"from": "00:00", "to": "45:00"},
        {"from": "40:00", "to": "90:00"}
    ]
    minutes = calculate_player_minutes(positions=positions, match_end_time="90:00")
    assert minutes == 90


def test_invalid_interval_is_discarded():
    positions = [{"from": "70:00", "to": "60:00"}]
    minutes = calculate_player_minutes(positions=positions, match_end_time="90:00")
    assert minutes == 0
