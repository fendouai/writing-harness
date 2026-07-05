from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


STOCK_PHRASES = [
    "it is important to note",
    "in today's fast-paced",
    "seamless user experience",
    "world-class",
    "innovative platform",
    "transform",
    "unlock efficiency",
    "strategic outcomes",
    "productive week",
    "learned a lot",
    "strong opportunities",
    "iterating thoughtfully",
]

WEAK_ENDINGS = [
    "we will continue",
    "moving forward",
    "going forward",
    "in conclusion",
    "to sum up",
    "overall",
]

ABSTRACT_TERMS = [
    "efficiency",
    "innovation",
    "value",
    "impact",
    "outcomes",
    "solution",
    "visibility",
    "friction",
    "synergy",
    "alignment",
]

CLAIM_MARKERS = [
    "should",
    "need",
    "do not need",
    "they need",
    "need to",
    "the point is",
    "the issue is",
    "the problem is",
    "the better move is",
    "recommend",
    "instead",
    "but",
    "because",
]

DISTINCTION_MARKERS = [
    "rather than",
    "instead of",
    "not",
    "unlike",
    "different from",
    "more than",
    "less than",
]

DEFAULT_ACTION_VERBS = [
    "write",
    "list",
    "choose",
    "compare",
    "test",
    "measure",
    "name",
    "review",
    "check",
    "decide",
    "count",
    "map",
    "use",
]

AGENCY_TERMS = [
    "choose",
    "decide",
    "build",
    "create",
    "control",
    "shape",
    "change",
    "reframe",
    "rewrite",
]

VICTIM_TERMS = [
    "stuck",
    "forced",
    "helpless",
    "confused",
    "blocked",
    "can't",
    "cannot",
    "no choice",
]

DEFAULT_MODULE_ORDER = [
    "M-01",
    "M-02",
    "M-03",
    "M-04",
    "M-05",
]

DEFAULT_MODULE_NAMES = {
    "M-01": "old-belief-index",
    "M-02": "expectation-break",
    "M-03": "new-framework",
    "M-04": "boundary-and-timing-anchor",
    "M-05": "identity-embed",
}


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str
    severity: str = "warn"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def split_paragraphs(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\n\s*\n", text.strip()) if part.strip()]


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def count_phrase(text: str, phrase: str) -> int:
    return normalize(text).count(normalize(phrase))


def count_any(text: str, phrases: list[str]) -> int:
    normalized = normalize(text)
    return sum(1 for phrase in phrases if normalize(phrase) in normalized)


def count_regex(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


def lint_writing(text: str) -> list[CheckResult]:
    checks: list[CheckResult] = []
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)
    first_span = " ".join(sentences[:2]) if sentences else text
    last_sentence = sentences[-1] if sentences else ""

    stock_hits = [phrase for phrase in STOCK_PHRASES if count_phrase(text, phrase) > 0]
    checks.append(
        CheckResult(
            name="stock_phrase_overuse",
            passed=not stock_hits,
            detail="no stock AI phrases detected" if not stock_hits else f"contains {', '.join(stock_hits[:4])}",
            severity="error",
        )
    )

    abstract_count = sum(count_phrase(text, term) for term in ABSTRACT_TERMS)
    checks.append(
        CheckResult(
            name="abstract_noun_pressure",
            passed=abstract_count <= max(2, word_count(text) // 80),
            detail=f"{abstract_count} abstract-term hits",
        )
    )

    lead_hits = [phrase for phrase in STOCK_PHRASES if count_phrase(first_span, phrase) > 0]
    checks.append(
        CheckResult(
            name="generic_opening",
            passed=not lead_hits,
            detail="opening is specific enough" if not lead_hits else f"generic opening via {', '.join(lead_hits[:3])}",
            severity="error",
        )
    )

    weak_ending_hits = [phrase for phrase in WEAK_ENDINGS if count_phrase(last_sentence, phrase) > 0]
    checks.append(
        CheckResult(
            name="weak_ending",
            passed=not weak_ending_hits,
            detail="ending lands on a point" if not weak_ending_hits else f"weak ending via {', '.join(weak_ending_hits)}",
            severity="error",
        )
    )

    claim_hits = count_any(text, CLAIM_MARKERS)
    checks.append(
        CheckResult(
            name="explicit_claim_signal",
            passed=claim_hits > 0,
            detail=f"{claim_hits} claim markers",
            severity="error",
        )
    )

    paragraph_lengths = [word_count(paragraph) for paragraph in paragraphs]
    flat_paragraphs = [length for length in paragraph_lengths if length < 14]
    checks.append(
        CheckResult(
            name="paragraph_substance",
            passed=len(flat_paragraphs) <= 1 or len(paragraphs) <= 2,
            detail=f"{len(flat_paragraphs)} thin paragraphs out of {len(paragraphs)}",
        )
    )

    return checks


def summarize_lint(checks: list[CheckResult]) -> dict:
    failed = [check for check in checks if not check.passed]
    error_count = sum(1 for check in failed if check.severity == "error")
    score = max(0, 100 - (error_count * 18) - ((len(failed) - error_count) * 8))
    return {
        "score": score,
        "passed": error_count == 0,
        "failed_checks": [check.name for check in failed],
        "checks": [check.__dict__ for check in checks],
    }


def evaluate_genre_contract(case: dict, text: str) -> list[CheckResult]:
    checks: list[CheckResult] = []
    for contract in case.get("genre_contracts", []):
        mode = contract["mode"]
        terms = contract["terms"]
        minimum = contract.get("min_hits", 1)
        hits = count_any(text, terms)
        passed = hits >= minimum
        checks.append(
            CheckResult(
                name=f"genre_contract:{contract['name']}",
                passed=passed,
                detail=f"{hits}/{minimum} contract hits for {contract['name']}",
                severity="error" if mode == "required" else "warn",
            )
        )
    return checks


TRACE_STAGE_NAMES = ["spec", "diagnose", "rewrite", "evaluate"]


def build_default_trace_template(case: dict) -> dict:
    return {
        "spec": {
            "reader": case["audience"],
            "objective": case["task"],
            "must_preserve": case["preserve_facts_all"],
            "must_avoid": case["avoid_phrases"],
        },
        "diagnose": {
            "failure_modes": [],
            "main_issue": "",
        },
        "rewrite": {
            "central_claim": "",
            "edits": [],
        },
        "evaluate": {
            "self_score": None,
            "remaining_risks": [],
        },
    }


def build_default_cw_artifact(case: dict) -> dict:
    return {
        "baseline": {
            "reader": case["audience"],
            "starting_state": {
                "K": case.get("starting_K", f"Reader starts with a blurred model of {case['surface']}."),
                "P": case.get("starting_P", "Reader leans on a weak or generic process."),
                "A": {
                    "emotion": case.get("starting_A_emotion", "skeptical"),
                    "resistance": case.get("starting_A_resistance", 7),
                    "attribution": case.get("starting_A_attribution", "external"),
                },
            },
            "target_state": {
                "K": case.get("target_K", case["task"]),
                "P": case.get("target_P", "Reader should leave with a sharper decision rule or tool."),
                "A": {
                    "emotion": case.get("target_A_emotion", "clear"),
                    "resistance": case.get("target_A_resistance", 3),
                    "attribution": case.get("target_A_attribution", "internal"),
                },
            },
            "displacement": {
                "K": "",
                "P": "",
                "A": "",
            },
        },
        "architecture": {
            "pattern": "AEH",
            "layers": {
                "assert": "",
                "exception": "",
                "handler": "",
                "log": "",
            },
        },
        "modules": [
            {
                "id": module_id,
                "name": DEFAULT_MODULE_NAMES[module_id],
                "ksa_targets": [],
                "input_state": "",
                "logic": [],
                "output_state": "",
                "interface_hook": "",
            }
            for module_id in DEFAULT_MODULE_ORDER
        ],
        "trace": build_default_trace_template(case),
        "unit_tests": {
            "K": {"passed": None, "notes": []},
            "P": {"passed": None, "notes": []},
            "A": {"passed": None, "notes": []},
        },
        "integration": {
            "passed": None,
            "notes": [],
        },
        "rollback": {
            "failed_dimension": "",
            "target_modules": [],
            "notes": [],
        },
    }


def cw_artifact_path_for_candidate(candidate_path: Path) -> Path:
    return candidate_path.with_suffix(".cw.json")


def load_cw_artifact_if_present(candidate_path: Path) -> dict | None:
    path = cw_artifact_path_for_candidate(candidate_path)
    if not path.exists():
        return None
    return json.loads(read_text(path))


def trace_path_for_candidate(candidate_path: Path) -> Path:
    return candidate_path.with_suffix(".trace.json")


def load_trace_if_present(candidate_path: Path) -> dict | None:
    cw_artifact = load_cw_artifact_if_present(candidate_path)
    if cw_artifact and isinstance(cw_artifact.get("trace"), dict):
        return cw_artifact["trace"]
    path = trace_path_for_candidate(candidate_path)
    if not path.exists():
        return None
    return json.loads(read_text(path))


def validate_trace_payload(trace: dict | None) -> list[CheckResult]:
    if trace is None:
        return [
            CheckResult(
                name="trace_present",
                passed=False,
                detail="missing trace file",
                severity="error",
            )
        ]

    checks = [
        CheckResult(
            name="trace_present",
            passed=True,
            detail="trace file present",
            severity="error",
        )
    ]
    for stage in TRACE_STAGE_NAMES:
        payload = trace.get(stage)
        checks.append(
            CheckResult(
                name=f"trace_stage:{stage}",
                passed=bool(payload),
                detail="present" if payload else "missing or empty",
                severity="error",
            )
        )

    diagnose_modes = trace.get("diagnose", {}).get("failure_modes", [])
    checks.append(
        CheckResult(
            name="trace_failure_modes",
            passed=len(diagnose_modes) > 0,
            detail=f"{len(diagnose_modes)} failure modes listed",
            severity="error",
        )
    )

    edits = trace.get("rewrite", {}).get("edits", [])
    checks.append(
        CheckResult(
            name="trace_edit_plan",
            passed=len(edits) > 0,
            detail=f"{len(edits)} edits listed",
            severity="error",
        )
    )

    self_score = trace.get("evaluate", {}).get("self_score")
    checks.append(
        CheckResult(
            name="trace_self_score",
            passed=isinstance(self_score, (int, float)),
            detail=f"self_score={self_score}",
            severity="warn",
        )
    )
    return checks


def _boolish(value: object) -> bool:
    return value not in (None, "", [], {})


def validate_cw_artifact(cw_artifact: dict | None) -> list[CheckResult]:
    if cw_artifact is None:
        return [
            CheckResult(
                name="cw_artifact_present",
                passed=False,
                detail="missing cw artifact",
                severity="error",
            )
        ]

    checks = [
        CheckResult("cw_artifact_present", True, "cw artifact present", "error"),
    ]

    baseline = cw_artifact.get("baseline", {})
    checks.append(CheckResult("cw_baseline_reader", _boolish(baseline.get("reader")), "reader present" if _boolish(baseline.get("reader")) else "missing reader", "error"))
    checks.append(CheckResult("cw_baseline_starting_state", _boolish(baseline.get("starting_state")), "starting_state present" if _boolish(baseline.get("starting_state")) else "missing starting_state", "error"))
    checks.append(CheckResult("cw_baseline_target_state", _boolish(baseline.get("target_state")), "target_state present" if _boolish(baseline.get("target_state")) else "missing target_state", "error"))

    architecture = cw_artifact.get("architecture", {})
    checks.append(
        CheckResult(
            "cw_architecture_pattern",
            architecture.get("pattern") == "AEH",
            f"pattern={architecture.get('pattern')}",
            "error",
        )
    )
    layers = architecture.get("layers", {})
    for layer in ["assert", "exception", "handler", "log"]:
        checks.append(
            CheckResult(
                name=f"cw_architecture_layer:{layer}",
                passed=_boolish(layers.get(layer)),
                detail="present" if _boolish(layers.get(layer)) else "missing or empty",
                severity="error",
            )
        )

    modules = cw_artifact.get("modules", [])
    checks.append(
        CheckResult(
            "cw_modules_count",
            len(modules) == 5,
            f"{len(modules)} modules",
            "error",
        )
    )
    module_ids = [module.get("id") for module in modules if isinstance(module, dict)]
    for module_id in DEFAULT_MODULE_ORDER:
        checks.append(
            CheckResult(
                name=f"cw_module:{module_id}",
                passed=module_id in module_ids,
                detail="present" if module_id in module_ids else "missing",
                severity="error",
            )
        )

    checks.extend(
        CheckResult(
            name=f"cw_unit_test:{dimension}",
            passed=_boolish(cw_artifact.get("unit_tests", {}).get(dimension)),
            detail="present" if _boolish(cw_artifact.get("unit_tests", {}).get(dimension)) else "missing",
            severity="warn",
        )
        for dimension in ["K", "P", "A"]
    )
    checks.append(
        CheckResult(
            "cw_integration",
            _boolish(cw_artifact.get("integration")),
            "present" if _boolish(cw_artifact.get("integration")) else "missing",
            "warn",
        )
    )
    checks.append(
        CheckResult(
            "cw_rollback",
            _boolish(cw_artifact.get("rollback")),
            "present" if _boolish(cw_artifact.get("rollback")) else "missing",
            "warn",
        )
    )
    checks.extend(validate_trace_payload(cw_artifact.get("trace")))
    return checks


def evaluate_module_coverage(cw_artifact: dict | None) -> list[CheckResult]:
    if cw_artifact is None:
        return [CheckResult("module_coverage", False, "missing cw artifact", "error")]

    checks: list[CheckResult] = []
    modules = {module.get("id"): module for module in cw_artifact.get("modules", []) if isinstance(module, dict)}
    for module_id in DEFAULT_MODULE_ORDER:
        module = modules.get(module_id, {})
        checks.append(
            CheckResult(
                name=f"module_logic:{module_id}",
                passed=bool(module.get("logic")) and _boolish(module.get("interface_hook")),
                detail="logic + interface present" if bool(module.get("logic")) and _boolish(module.get("interface_hook")) else "missing logic or interface",
                severity="error",
            )
        )
    return checks


def evaluate_cognitive_dimensions(case: dict, text: str, cw_artifact: dict | None) -> list[CheckResult]:
    targets = case.get("cognitive_targets", {})
    checks: list[CheckResult] = []

    k_targets = targets.get("K", {})
    distinction_terms = k_targets.get("distinction_markers_any", DISTINCTION_MARKERS)
    distinction_hits = count_any(text, distinction_terms)
    min_distinctions = k_targets.get("min_distinctions", 1)
    checks.append(
        CheckResult(
            "K_distinction_precision",
            distinction_hits >= min_distinctions,
            f"{distinction_hits}/{min_distinctions} distinction markers",
            "error",
        )
    )
    action_terms = k_targets.get("action_verbs_any", DEFAULT_ACTION_VERBS)
    action_hits = count_any(text, action_terms)
    min_actions = k_targets.get("min_action_verbs", 2)
    checks.append(
        CheckResult(
            "K_action_granularity",
            action_hits >= min_actions,
            f"{action_hits}/{min_actions} action verbs",
            "warn",
        )
    )

    p_targets = targets.get("P", {})
    if_then_hits = count_regex(text, r"\b(if|when)\b")
    min_if_then = p_targets.get("if_then_min", 1)
    checks.append(
        CheckResult(
            "P_decision_density",
            if_then_hits >= min_if_then,
            f"{if_then_hits}/{min_if_then} decision markers",
            "error",
        )
    )
    template_hits = count_regex(text, r"_{3,}|\[[ xX]?\]")
    needs_template = p_targets.get("requires_template", False)
    checks.append(
        CheckResult(
            "P_tool_delivery",
            (template_hits > 0) if needs_template else True,
            f"template hits={template_hits}",
            "error" if needs_template else "warn",
        )
    )
    process_terms = p_targets.get("process_terms_any", [])
    process_hits = count_any(text, process_terms) if process_terms else 0
    process_min = p_targets.get("min_process_terms", 0)
    checks.append(
        CheckResult(
            "P_process_cues",
            process_hits >= process_min,
            f"{process_hits}/{process_min} process cues",
            "warn",
        )
    )

    a_targets = targets.get("A", {})
    agency_terms = a_targets.get("agency_terms_any", AGENCY_TERMS)
    victim_terms = a_targets.get("victim_terms_any", VICTIM_TERMS)
    attribution_shift = count_any(text, agency_terms) - count_any(text, victim_terms)
    checks.append(
        CheckResult(
            "A_attribution_shift",
            attribution_shift > 0,
            f"net shift={attribution_shift}",
            "error",
        )
    )

    resistance_check = CheckResult("A_resistance_drop", True, "not evaluated", "warn")
    if cw_artifact:
        start_resistance = cw_artifact.get("baseline", {}).get("starting_state", {}).get("A", {}).get("resistance")
        target_resistance = cw_artifact.get("baseline", {}).get("target_state", {}).get("A", {}).get("resistance")
        actual_resistance = cw_artifact.get("trace", {}).get("evaluate", {}).get("resistance_after")
        min_drop = a_targets.get("min_resistance_drop", 2)
        if isinstance(start_resistance, (int, float)) and isinstance(actual_resistance, (int, float)):
            drop = start_resistance - actual_resistance
            resistance_check = CheckResult(
                "A_resistance_drop",
                drop >= min_drop and (target_resistance is None or actual_resistance <= target_resistance),
                f"start={start_resistance}, after={actual_resistance}, drop={drop}",
                "warn",
            )
    checks.append(resistance_check)
    return checks
