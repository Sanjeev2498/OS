#!/usr/bin/env python3
"""Task 5: Paging and Segmentation (5 marks)."""

from typing import List, Optional, Tuple


def parse_page_table(values: str) -> List[Optional[int]]:
    """Parse comma-separated frame numbers; X denotes an unmapped page."""
    entries = []
    for value in values.split(","):
        value = value.strip()
        if value.lower() == "x":
            entries.append(None)
        else:
            frame = int(value)
            if frame < 0:
                raise ValueError("Frame numbers must be zero or greater.")
            entries.append(frame)
    if not entries:
        raise ValueError("The page table cannot be empty.")
    return entries


def translate_page(
    logical_address: int,
    page_size: int,
    page_table: List[Optional[int]],
) -> Tuple[int, int, int, int]:
    if page_size <= 0:
        raise ValueError("Page size must be greater than zero.")
    if logical_address < 0:
        raise ValueError("Logical address cannot be negative.")

    page_number = logical_address // page_size
    offset = logical_address % page_size
    if page_number >= len(page_table):
        raise ValueError(f"Page {page_number} is outside the page table.")

    frame_number = page_table[page_number]
    if frame_number is None:
        raise ValueError(f"Page {page_number} is unmapped.")

    physical_address = frame_number * page_size + offset
    return page_number, offset, frame_number, physical_address


def translate_segment(
    segment_number: int, offset: int, base: int, limit: int
) -> int:
    if segment_number < 0:
        raise ValueError("Segment number cannot be negative.")
    if base < 0:
        raise ValueError("Segment base cannot be negative.")
    if limit <= 0:
        raise ValueError("Segment limit must be greater than zero.")
    if offset < 0 or offset >= limit:
        raise ValueError(f"Invalid segment reference: offset must be in [0, {limit}).")
    return base + offset


def read_integer(prompt: str) -> int:
    return int(input(prompt).strip())


def main() -> None:
    print("=" * 64)
    print("TASK 5: PAGING AND SEGMENTATION")
    print("=" * 64)

    try:
        page_size = read_integer("Enter page size: ")
        page_table = parse_page_table(
            input("Enter page-table frame numbers (comma-separated; X = unmapped): ")
        )
        logical_address = read_integer("Enter logical address: ")

        print("\nPAGING TRANSLATION")
        if page_size <= 0:
            raise ValueError("Page size must be greater than zero.")
        if logical_address < 0:
            raise ValueError("Logical address cannot be negative.")

        page_number = logical_address // page_size
        offset = logical_address % page_size
        print(f"Page number = {logical_address} // {page_size} = {page_number}")
        print(f"Offset = {logical_address} % {page_size} = {offset}")

        try:
            translated_page, translated_offset, frame, physical = translate_page(
                logical_address, page_size, page_table
            )
            print(f"Page-table entry P[{translated_page}] = frame {frame} (valid)")
            print(
                f"Physical address = frame * page size + offset"
                f" = {frame} * {page_size} + {translated_offset} = {physical}"
            )
        except ValueError as error:
            print(f"Paging translation rejected: {error}")

        print("\nSEGMENTATION TRANSLATION")
        segment_number = read_integer("Enter segment number: ")
        offset = read_integer("Enter segment offset: ")
        base = read_integer("Enter segment base: ")
        limit = read_integer("Enter segment limit: ")
        print(
            f"Validate segment S{segment_number}: "
            f"0 <= offset ({offset}) < limit ({limit})"
        )
        try:
            physical = translate_segment(segment_number, offset, base, limit)
            print(f"Segment reference is valid.")
            print(
                f"Physical address = base + offset = {base} + {offset} = {physical}"
            )
        except ValueError as error:
            print(f"Segmentation translation rejected: {error}")
    except ValueError as error:
        print(f"Input error: {error}")


if __name__ == "__main__":
    main()
