from typing import Dict, List


def cleanupDanglingCuts(old_cuts: Dict[str, List[str]]) -> Dict[str, List[str]]:
    new_cuts: Dict[str, List[str]] = {}
    for signal in old_cuts:
        if len(old_cuts[signal]) == 0:
            continue
        if len(old_cuts[signal]) == 1 and old_cuts[signal][0] == signal:
            continue
        new_cuts[signal] = old_cuts[signal][:]
    return new_cuts
