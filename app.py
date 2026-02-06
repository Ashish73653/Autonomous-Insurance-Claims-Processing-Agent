import json
import sys
from extractor import extract_text, extract_fields
from validator import find_missing_fields, validate_consistency
from router import route_claim


def main():
    print("Autonomous Insurance Claims Processing Agent")

    # -------------------------
    # CLI Argument Handling
    # -------------------------
    if len(sys.argv) < 2:
        print("Usage: python app.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        text = extract_text(file_path)
        data = extract_fields(text)

        missing = find_missing_fields(data)
        inconsistencies = validate_consistency(data)

        route, reasoning, confidence = route_claim(data, missing, inconsistencies)

        # Final required output format
        output = {
            "extractedFields": data,
            "missingFields": missing,
            "recommendedRoute": route,
            "reasoning": reasoning,
            "confidenceScore": confidence
        }

        print("\n--- FINAL OUTPUT ---\n")
        print(json.dumps(output, indent=4))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
