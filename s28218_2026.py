# Album number: s28218
# Date: 2026-05-15
# Description: Random DNA sequence generator in FASTA format
# with statistics, motif search, reverse complement,
# transcription and configurable nucleotide distribution.

import random
from collections import Counter

NUCLEOTIDES = ["A", "C", "G", "T"]


def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100_000) -> int:
    """
    Gets an integer from the user within a specified range.

    Repeats the question until a valid value is provided.
    """

    while True:
        try:
            value = int(input(prompt))

            if min_val <= value <= max_val:
                return value

            print(
                f"Error: value must be an integer "
                f"in the range [{min_val}, {max_val}]."
            )

        except ValueError:
            print(
                f"Error: value must be an integer "
                f"in the range [{min_val}, {max_val}]."
            )


def generate_sequence(length: int,
                      weights: dict | None = None) -> str:
    """
    Returns a random DNA sequence of the specified length.

    Optional weights allow configurable nucleotide distribution.
    """

    if weights is None:
        weights = {
            "A": 25,
            "C": 25,
            "G": 25,
            "T": 25
        }

    sequence = "".join(
        random.choices(
            population=NUCLEOTIDES,
            weights=[
                weights["A"],
                weights["C"],
                weights["G"],
                weights["T"]
            ],
            k=length
        )
    )

    return sequence


def calculate_stats(sequence: str) -> dict:
    """
    Returns sequence statistics.

    Keys:
    "A", "C", "G", "T" -> percentage values
    "GC" -> GC-content percentage
    """

    stats = {}

    total = len(sequence)

    for nucleotide in NUCLEOTIDES:
        count = sequence.count(nucleotide)
        stats[nucleotide] = (count / total) * 100

    gc_content = (
        sequence.count("G") +
        sequence.count("C")
    ) / total * 100

    stats["GC"] = gc_content

    return stats


def insert_name(sequence: str, name: str) -> str:
    """
    Inserts a name at a random position in the sequence.

    The inserted name is written in lowercase letters.
    """

    position = random.randint(0, len(sequence))

    return (
        sequence[:position]
        + name.lower()
        + sequence[position:]
    )


def format_fasta(seq_id: str,
                 description: str,
                 sequence: str,
                 line_width: int = 80) -> str:
    """
    Returns a formatted FASTA record as a string.
    """

    header = f">{seq_id}"

    if description:
        header += f" {description}"

    fasta_lines = [header]

    # Split sequence into fixed-width lines
    for i in range(0, len(sequence), line_width):
        fasta_lines.append(
            sequence[i:i + line_width]
        )

    return "\n".join(fasta_lines)


def save_to_file(filename: str, content: str):
    """
    Saves text content to a file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


# =========================
# ADDITIONAL FUNCTIONALITIES
# =========================

def get_nucleotide_distribution() -> dict:
    """
    Gets nucleotide percentages from the user.

    The sum must equal 100.
    """

    while True:
        print("\nEnter nucleotide distribution (%):")

        try:
            a = float(input("A: "))
            c = float(input("C: "))
            g = float(input("G: "))
            t = float(input("T: "))

            total = a + c + g + t

            if total == 100:
                return {
                    "A": a,
                    "C": c,
                    "G": g,
                    "T": t
                }

            print("Error: percentages must sum to 100.")

        except ValueError:
            print("Error: enter numeric values.")


def search_motif(sequence: str, motif: str) -> list:
    """
    Searches for all motif occurrences in the sequence.

    Positions use biological indexing (starting from 1).
    """

    positions = []

    for i in range(len(sequence) - len(motif) + 1):

        if sequence[i:i + len(motif)] == motif:
            positions.append(i + 1)

    return positions


def get_complement(sequence: str) -> str:
    """
    Returns the complementary DNA strand.
    """

    complement_map = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }

    return "".join(
        complement_map[nucleotide]
        for nucleotide in sequence
    )


def get_reverse_complement(sequence: str) -> str:
    """
    Returns the reverse complementary DNA strand.
    """

    complement = get_complement(sequence)

    return complement[::-1]


def transcribe_dna(sequence: str) -> str:
    """
    Converts DNA to mRNA.

    Replaces T with U.
    """

    return sequence.replace("T", "U")


def main():
    """
    Main program function.
    """

    # Get sequence length
    length = validate_positive_int(
        "Enter sequence length: "
    )

    # Validate sequence ID
    while True:
        sequence_id = input(
            "Enter sequence ID: "
        ).strip()

        if sequence_id and " " not in sequence_id:
            break

        print("Invalid sequence ID.")

    # Optional FASTA description
    description = input(
        "Enter sequence description: "
    ).strip()

    # User name for insertion
    user_name = input(
        "Enter your name: "
    ).strip()

    # Configure nucleotide distribution
    custom_distribution = input(
        "Custom nucleotide distribution? (y/n): "
    ).strip().lower()

    if custom_distribution == "y":
        weights = get_nucleotide_distribution()
    else:
        weights = None

    # Generate DNA sequence
    dna_sequence = generate_sequence(
        length,
        weights
    )

    # Calculate statistics BEFORE name insertion
    stats = calculate_stats(dna_sequence)

    # Insert user name
    modified_sequence = insert_name(
        dna_sequence,
        user_name
    )

    # Generate reverse complement
    reverse_complement = get_reverse_complement(
        dna_sequence
    )

    # Generate mRNA
    mrna_sequence = transcribe_dna(
        dna_sequence
    )

    # Search for motif
    motif = input(
        "Enter motif to search (optional): "
    ).strip().upper()

    motif_positions = []

    if motif:
        motif_positions = search_motif(
            dna_sequence,
            motif
        )

    # Prepare FASTA records
    fasta_records = []

    fasta_records.append(
        format_fasta(
            sequence_id,
            description,
            modified_sequence
        )
    )

    fasta_records.append(
        format_fasta(
            sequence_id + "_revcomp",
            "reverse complement",
            reverse_complement
        )
    )

    fasta_records.append(
        format_fasta(
            sequence_id + "_mRNA",
            "transcribed mRNA",
            mrna_sequence
        )
    )

    fasta_text = "\n".join(fasta_records)

    # Save FASTA file
    output_file = f"{sequence_id}.fasta"

    save_to_file(
        output_file,
        fasta_text
    )

    # Print statistics
    print(f"\nSequence saved to file: {output_file}")

    print(f"\nSequence statistics (n={length}):")

    for nucleotide in NUCLEOTIDES:
        print(
            f"{nucleotide}: "
            f"{stats[nucleotide]:.2f}%"
        )

    print(
        f"GC-content: "
        f"{stats['GC']:.2f}%"
    )

    # Print motif search results
    if motif:

        if motif_positions:
            print(
                f"\nMotif '{motif}' found at positions:"
            )
            print(", ".join(map(str, motif_positions)))

        else:
            print(
                f"\nMotif '{motif}' not found."
            )


if __name__ == "__main__":
    main()