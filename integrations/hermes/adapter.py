from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List


def _env_enabled(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class ArgusHermesAdapter:
    agent_id: str = "argus"
    enabled_env: str = "HERMES_ENABLED"

    def __post_init__(self) -> None:
        self.enabled = _env_enabled(self.enabled_env, "false")
        self._client = None
        if self.enabled:
            from integrations.hermes_client import HermesClient  # type: ignore

            self._client = HermesClient()

    def register(self, capabilities: Iterable[str]) -> None:
        if self._client is None:
            return
        self._client.register_agent(self.agent_id, capabilities)

    def load_memory(self) -> Dict[str, Any]:
        if self._client is None:
            return {}
        return self._client.load_memory(self.agent_id)

    def save_verification_result(self, verification_payload: Dict[str, Any]) -> None:
        if self._client is None:
            return
        existing = self._client.load_memory(self.agent_id)
        existing.setdefault("verification_results", [])
        existing["verification_results"].append(verification_payload)
        self._client.save_memory(self.agent_id, existing)

    def recover(self, error_context: Dict[str, Any], retry_fn: Callable[[], Any]) -> Any:
        if self._client is None:
            raise RuntimeError("Hermes recovery called while disabled")
        return self._client.self_heal(error_context, retry_fn)


def gate_then_run(
    governance_checks: Iterable[Callable[[], Dict[str, Any]]],
    hermes_action: Callable[[], Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Governance-first wrapper.

    Argus checks run before any Hermes-initiated external action.
    """
    adapter = ArgusHermesAdapter()
    adapter.register(
        capabilities=[
            "governance-gate",
            "verification-loop",
            "secret-scanning",
            "compliance-enforcement",
        ]
    )

    check_results: List[Dict[str, Any]] = []
    for check in governance_checks:
        result = check()
        check_results.append(result)
        if not result.get("passed", False):
            blocked = {
                "status": "blocked",
                "reason": "governance_check_failed",
                "check_result": result,
            }
            adapter.save_verification_result(blocked)
            return blocked

    def _run_action() -> Dict[str, Any]:
        action_result = hermes_action()
        payload = {
            "status": "passed",
            "governance_checks": check_results,
            "action_result": action_result,
        }
        adapter.save_verification_result(payload)
        return payload

    try:
        return _run_action()
    except Exception as exc:
        if not adapter.enabled:
            raise
        return adapter.recover(
            {
                "agent_id": "argus",
                "error": str(exc),
                "governance_checks": check_results,
            },
            _run_action,
        )
