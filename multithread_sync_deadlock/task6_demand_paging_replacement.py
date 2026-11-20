#!/usr/bin/env python3
"""Task 6: Demand Paging, Page Replacement and Thrashing (5 marks)."""

from typing import Dict, List, Optional, Tuple

ALGORITHMS = ("FIFO", "LRU", "Optimal")


def simulate(
    references: List[int], frame_count: int, algorithm: str
) -> Tuple[List[Tuple[int, bool, List[Optional[int]]]], int, int]:
    """Return per-reference (page, hit, frame-state) rows and totals."""
    algorithm = next(
        (name for name in ALGORITHMS if name.lower() == algorithm.lower()), algorithm
    )
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    if frame_count <= 0:
        raise ValueError("Frame count must be greater than zero.")
    if any(page < 0 for page in references):
        raise ValueError("Page numbers must be zero or greater.")

    frames: List[Optional[int]] = [None] * frame_count
    last_used: Dict[int, int] = {}
    fifo_next = 0
    hits = 0
    faults = 0
    rows = []

    for position, page in enumerate(references):
        if page in frames:
            hit = True
            hits += 1
        else:
            hit = False
            faults += 1

            if None in frames:
                slot = frames.index(None)
            elif algorithm == "FIFO":
                slot = fifo_next
                fifo_next = (fifo_next + 1) % frame_count
            elif algorithm == "LRU":
                victim = min(frames, key=lambda resident: last_used[resident])
                slot = frames.index(victim)
            else:
                future = references[position + 1 :]

                def next_use(resident: Optional[int]) -> float:
                    try:
                        return future.index(resident)
                    except ValueError:
                        return float("inf")

                victim = max(frames, key=next_use)
                slot = frames.index(victim)

            frames[slot] = page

        last_used[page] = position
        rows.append((page, hit, frames.copy()))

    return rows, hits, faults


def display_result(
    references: List[int], frame_count: int, algorithm: str
) -> Tuple[int, int]:
    rows, hits, faults = simulate(references, frame_count, algorithm)
    print(f"\n{algorithm} with {frame_count} frame(s)")
    print(f"{'Ref':>6}  {'Result':<8}  Frame state")
    print("-" * 46)
    for page, hit, frames in rows:
        state = " ".join("-" if value is None else str(value) for value in frames)
        print(f"{page:>6}  {'HIT' if hit else 'FAULT':<8}  [{state}]")

    total = len(references)
    hit_ratio = hits / total if total else 0.0
    fault_ratio = faults / total if total else 0.0
    print(f"Total hits: {hits}")
    print(f"Total page faults: {faults}")
    print(f"Hit ratio: {hits}/{total} = {hit_ratio:.2%}")
    print(f"Fault ratio: {faults}/{total} = {fault_ratio:.2%}")
    return hits, faults


def main() -> None:
    print("=" * 72)
    print("TASK 6: DEMAND PAGING, PAGE REPLACEMENT AND THRASHING")
    print("=" * 72)

    try:
        references = [
            int(value)
            for value in input("Enter page reference string (space/comma-separated): ")
            .replace(",", " ")
            .split()
        ]
        if not references:
            raise ValueError("The reference string cannot be empty.")
        if any(page < 0 for page in references):
            raise ValueError("Page numbers must be zero or greater.")

        frame_counts = [
            int(value)
            for value in input(
                "Enter one or more frame counts (comma-separated): "
            ).split(",")
        ]
        if not frame_counts or any(count <= 0 for count in frame_counts):
            raise ValueError("Enter one or more positive frame counts.")

        for frame_count in frame_counts:
            print(f"\n{'=' * 72}")
            print(f"Reference string: {references} | Frames: {frame_count}")
            results = {}
            for algorithm in ALGORITHMS:
                results[algorithm] = display_result(
                    references, frame_count, algorithm
                )

            print("\nAlgorithm comparison (fewer faults is better):")
            for algorithm in ALGORITHMS:
                hits, faults = results[algorithm]
                print(f"{algorithm:<8} hits={hits:<4} faults={faults}")
            best_faults = min(faults for _, faults in results.values())
            best = [
                algorithm
                for algorithm, (_, faults) in results.items()
                if faults == best_faults
            ]
            print(f"Best result for this frame count: {', '.join(best)}")

            highest_faults = max(faults for _, faults in results.values())
            highest_ratio = highest_faults / len(references)
            if highest_ratio >= 0.75:
                print(
                    "High page-fault case: this high fault ratio is a simplified "
                    "example of thrashing."
                )
            else:
                print(
                    f"Highest tested fault ratio is {highest_ratio:.2%}; "
                    "this run does not meet the 75% high-fault indicator."
                )

        print("\nSimplified thrashing example (cyclic working set of 3 pages, 2 frames):")
        demo_references = [1, 2, 3] * 4
        _, _, demo_faults = simulate(demo_references, 2, "FIFO")
        print(
            f"FIFO references {demo_references} with 2 frames: "
            f"{demo_faults}/{len(demo_references)} faults "
            f"({demo_faults / len(demo_references):.2%})."
        )
        print(
            "The repeated working set does not fit in memory, so pages are "
            "continually replaced; this is a simplified thrashing example."
        )
    except ValueError as error:
        print(f"Input error: {error}")


if __name__ == "__main__":
    main()
