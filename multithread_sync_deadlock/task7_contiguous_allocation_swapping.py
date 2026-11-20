#!/usr/bin/env python3
"""Task 7: Contiguous Allocation, Swapping and Address Translation (5 marks)."""

from typing import List, Optional, Tuple

METHODS = ("First Fit", "Best Fit", "Worst Fit")


def choose_block(
    remaining: List[int],
    occupied: List[Optional[int]],
    process_size: int,
    method: str,
) -> Optional[int]:
    method = method.title()
    if method not in METHODS:
        raise ValueError(f"Unknown allocation method: {method}")
    candidates = [
        index
        for index, size in enumerate(remaining)
        if occupied[index] is None and size >= process_size
    ]
    if not candidates:
        return None
    if method == "First Fit":
        return candidates[0]
    if method == "Best Fit":
        return min(candidates, key=lambda index: remaining[index])
    return max(candidates, key=lambda index: remaining[index])


def allocate_processes(
    block_sizes: List[int], process_sizes: List[int], method: str
) -> Tuple[List[Optional[int]], List[int]]:
    if any(size <= 0 for size in block_sizes + process_sizes):
        raise ValueError("Block and process sizes must be greater than zero.")

    remaining = block_sizes.copy()
    occupied: List[Optional[int]] = [None] * len(block_sizes)
    for process_index, process_size in enumerate(process_sizes):
        block_index = choose_block(remaining, occupied, process_size, method)
        if block_index is not None:
            occupied[block_index] = process_index
            remaining[block_index] -= process_size
    return occupied, remaining


def translate_address(base: int, limit: int, logical_address: int) -> int:
    if base < 0:
        raise ValueError("Base cannot be negative.")
    if limit <= 0:
        raise ValueError("Limit must be greater than zero.")
    if logical_address < 0 or logical_address >= limit:
        raise ValueError(f"Logical address must be in [0, {limit}).")
    return base + logical_address


def display_memory(
    block_sizes: List[int],
    process_sizes: List[int],
    occupied: List[Optional[int]],
    remaining: List[int],
    title: str,
) -> None:
    print(f"\n{title}")
    print(f"{'Block':<10}{'Size':<10}{'Process':<12}{'Remaining':<12}")
    print("-" * 44)
    for index, owner in enumerate(occupied):
        process = "Free" if owner is None else f"P{owner + 1} ({process_sizes[owner]})"
        print(
            f"B{index + 1:<9}{block_sizes[index]:<10}"
            f"{process:<12}{remaining[index]:<12}"
        )
    allocated = {
        owner for owner in occupied if owner is not None
    }
    for process_index, size in enumerate(process_sizes):
        if process_index not in allocated:
            print(f"P{process_index + 1} ({size}) is unallocated.")


def simulate_swap(
    block_sizes: List[int],
    process_sizes: List[int],
    occupied: List[Optional[int]],
    remaining: List[int],
    outgoing_process: int,
    incoming_size: int,
    method: str,
) -> Tuple[List[Optional[int]], List[int], Optional[int]]:
    if incoming_size <= 0:
        raise ValueError("Incoming process size must be greater than zero.")
    outgoing_index = outgoing_process - 1
    if outgoing_index < 0 or outgoing_index >= len(process_sizes):
        raise ValueError("Outgoing process number is outside the process list.")

    new_occupied = occupied.copy()
    new_remaining = remaining.copy()
    outgoing_block = next(
        (index for index, owner in enumerate(new_occupied) if owner == outgoing_index),
        None,
    )
    if outgoing_block is None:
        raise ValueError(f"P{outgoing_process} is not currently allocated.")

    print(f"Releasing P{outgoing_process} from B{outgoing_block + 1}.")
    new_occupied[outgoing_block] = None
    new_remaining[outgoing_block] = block_sizes[outgoing_block]

    incoming_block = choose_block(
        new_remaining, new_occupied, incoming_size, method
    )
    if incoming_block is not None:
        new_occupied[incoming_block] = len(process_sizes)
        new_remaining[incoming_block] -= incoming_size
        process_sizes.append(incoming_size)
    return new_occupied, new_remaining, incoming_block


def main() -> None:
    print("=" * 72)
    print("TASK 7: CONTIGUOUS ALLOCATION, SWAPPING AND ADDRESS TRANSLATION")
    print("=" * 72)
    try:
        block_sizes = [
            int(value)
            for value in input("Enter memory-block sizes (comma-separated): ").split(",")
        ]
        process_sizes = [
            int(value)
            for value in input("Enter process sizes (comma-separated): ").split(",")
        ]
        if not block_sizes or not process_sizes:
            raise ValueError("Enter at least one memory block and one process.")
        if any(size <= 0 for size in block_sizes + process_sizes):
            raise ValueError("Block and process sizes must be greater than zero.")

        allocations = {}
        print("\nCONTIGUOUS MEMORY ALLOCATION")
        for method in METHODS:
            # Each strategy starts with fresh block data.
            occupied, remaining = allocate_processes(
                block_sizes.copy(), process_sizes.copy(), method
            )
            allocations[method] = (occupied, remaining)
            display_memory(
                block_sizes,
                process_sizes,
                occupied,
                remaining,
                f"{method} allocation",
            )

        print("\nADDRESS TRANSLATION")
        base = int(input("Enter Base: ").strip())
        limit = int(input("Enter Limit: ").strip())
        logical_address = int(input("Enter Logical Address: ").strip())
        print(
            f"Validate: 0 <= logical address ({logical_address}) < limit ({limit})"
        )
        try:
            physical = translate_address(base, limit, logical_address)
            print(
                f"Physical address = base + logical address"
                f" = {base} + {logical_address} = {physical}"
            )
        except ValueError as error:
            print(f"Address translation rejected: {error}")

        print("\nSWAPPING SIMULATION")
        method = input("Choose allocation method (First Fit/Best Fit/Worst Fit): ").strip()
        if method.title() not in allocations:
            raise ValueError("Choose First Fit, Best Fit, or Worst Fit.")
        occupied, remaining = allocations[method.title()]
        display_memory(
            block_sizes,
            process_sizes,
            occupied,
            remaining,
            "Memory before swap",
        )
        outgoing = int(input("Enter outgoing process number (P number): ").strip())
        incoming_size = int(input("Enter incoming process size: ").strip())
        occupied_after, remaining_after, incoming_block = simulate_swap(
            block_sizes,
            process_sizes,
            occupied,
            remaining,
            outgoing,
            incoming_size,
            method.title(),
        )
        if incoming_block is None:
            print(f"Incoming process of size {incoming_size} could not be allocated.")
        else:
            print(
                f"Incoming P{len(process_sizes)} allocated to B{incoming_block + 1}."
            )
        display_memory(
            block_sizes,
            process_sizes,
            occupied_after,
            remaining_after,
            "Memory after swap",
        )
    except ValueError as error:
        print(f"Input/allocation error: {error}")


if __name__ == "__main__":
    main()
