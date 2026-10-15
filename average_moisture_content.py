import pandas as pd
# Write here the file that was written by the simulation program
input_file = "Section_adsorption_65_90.rno"
# Write here the output file
output_file = "average_mc_section_adsorption_2nd_column.csv"

results = []

with open(input_file, "r") as f:

    while True:

        # Read section header
        header = f.readline()

        # End of file
        if not header:
            break

        header = header.strip()

        # Ignore empty lines
        if not header:
            continue

        # Header:
        # 16508 increment_number
        parts = header.split()

        try:
            number_of_lines = int(parts[0])
            increment = int(parts[1])
        except (ValueError, IndexError):
            print(f"Warning: invalid section header: {header}")
            continue

        # Read the data

        values = []
        ignored_lines = 0

        for _ in range(min(16504, number_of_lines)):

            line = f.readline()

            if not line:
                break

            parts = line.split()

            # Make sure there are at least two columns
            if len(parts) < 2:
                ignored_lines += 1
                continue

            # Try to convert second column to a number
            try:
                value = float(parts[1])
                values.append(value)

            except ValueError:
                # Invalid value -> ignore this line
                ignored_lines += 1
                print(
                    f"Increment {increment}: "
                    f"ignored invalid value: {parts[1]}"
                )

        # Calculate average

        if values:
            average = sum(values) / len(values)

            results.append([increment, average])

            print(
                f"Increment {increment}: "
                f"{len(values)} valid values, "
                f"{ignored_lines} ignored, "
                f"average = {average:.6f}"
            )

        else:
            print(
                f"Increment {increment}: "
                f"No valid values found."
            )

# Save results

df = pd.DataFrame(
    results,
    columns=["Increment", "Average"]
)

df.to_csv(output_file, index=False)

print("\nResults saved to:", output_file)
