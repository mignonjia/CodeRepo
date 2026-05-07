from __future__ import annotations

import unittest

from core.clip import parse_model_response
from games import get_game_spec, list_game_keys, resolve_game_selection
from llm import build_model_client, resolve_model_provider, validate_model_thinking_mode


class SmokeTests(unittest.TestCase):
    def test_registered_games_and_selection_aliases(self) -> None:
        """Check that core games and aliases are registered."""
        self.assertIn("breakout", list_game_keys())
        self.assertIn("assault", list_game_keys())
        self.assertEqual(resolve_game_selection("selected"), ["breakout", "assault"])

    def test_response_parser_maps_actions(self) -> None:
        """Check that parser output maps to expected action ids."""
        spec = get_game_spec("breakout")
        parsed = parse_model_response(
            "thought: track the ball\nmove: [left, right]",
            game_spec=spec,
            max_actions=10,
        )
        self.assertTrue(parsed.is_valid, parsed.errors)
        self.assertEqual(parsed.action_ids, [3, 2])

    def test_random_client_is_available_without_api_keys(self) -> None:
        """Check that the local random client works without provider keys."""
        validate_model_thinking_mode("random", "off")
        self.assertEqual(resolve_model_provider(model_name="random", provider="auto"), "random")
        response = build_model_client("random").generate_turn(
            prompt_text="Available actions:\n- noop: no action\n- left: move left\n",
            model_name="random",
            thinking_mode="off",
        )
        self.assertIn("move:", response.text)


if __name__ == "__main__":
    unittest.main()
