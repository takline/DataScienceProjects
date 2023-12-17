import pandas as pd
import json
from collections import defaultdict


def process_flight_data(csv_file_path, output_csv_path, output_json_path):
    # Read CSV data
    df = pd.read_csv(csv_file_path, encoding="utf-8")

    # Generate flight ID
    df["flight_id"] = (
        df["FL_NUM"].astype(str)
        + df["ORIGIN"]
        + df["CRS_DEP_TIME"].astype(str)
        + df["FL_DATE"]
    )
    flight_dict = df.set_index("flight_id").to_dict(orient="index")

    # Initialize master dictionary
    master_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Process flight data
    for flight_id, flight_info in flight_dict.items():
        origin = flight_info["ORIGIN"]
        dest = flight_info["DEST"]
        master_dict[origin][dest]["count"] += 1

        # Calculate travel time and experience
        if flight_info["CANCELLED"]:
            travel_time = 0
            experience = -flight_info["CRS_ELAPSED_TIME"]
        elif flight_info["DIVERTED"]:
            travel_time = flight_info["CRS_ELAPSED_TIME"]
            experience = -flight_info["DEP_DELAY_NEW"] - flight_info["CRS_ELAPSED_TIME"]
        else:
            travel_time = flight_info["ACTUAL_ELAPSED_TIME"]
            experience = -flight_info["ARR_DELAY"]

        master_dict[origin][dest]["travel_time"] += travel_time
        master_dict[origin][dest]["experience"] += experience

    # Calculate experience scores
    for origin in master_dict:
        for dest in master_dict[origin]:
            total_flight_time = master_dict[origin][dest]["travel_time"]
            total_experience = master_dict[origin][dest]["experience"]
            master_dict[origin][dest]["experience_score"] = (
                total_experience / total_flight_time if total_flight_time else 0
            )

    # Create DataFrame from master_dict
    unleveled_df = pd.DataFrame(
        [
            {"origin": origin, "destination": dest, **values}
            for origin, destinations in master_dict.items()
            for dest, values in destinations.items()
        ]
    )

    # Save processed data to CSV
    unleveled_df.to_csv(output_csv_path, index=False)

    # Generate JSON data for visualization
    airlines = set(df["CARRIER"])
    dates = sorted(set(df["FL_DATE"].apply(lambda x: int(x[2:].replace("/15", "")))))

    flight_count, scoring, total_time, final_exp = (
        defaultdict(int),
        defaultdict(int),
        defaultdict(int),
        defaultdict(int),
    )

    for flight_id, flight_info in flight_dict.items():
        airline = flight_info["CARRIER"]
        date = int(flight_info["FL_DATE"][2:].replace("/15", ""))

        flight_count[(airline, date)] += 1
        experience = (
            -flight_info["ARR_DELAY"]
            if not flight_info["CANCELLED"] and not flight_info["DIVERTED"]
            else -flight_info["CRS_ELAPSED_TIME"]
        )
        scoring[(airline, date)] += experience
        travel_time = (
            flight_info["ACTUAL_ELAPSED_TIME"]
            if not flight_info["CANCELLED"] and not flight_info["DIVERTED"]
            else 0
        )
        total_time[(airline, date)] += travel_time

    # Calculate final experience score
    for (airline, date), experience in scoring.items():
        total_flight_time = total_time[(airline, date)]
        final_exp[(airline, date)] = (
            experience / total_flight_time if total_flight_time else 0
        )

    # Create final JSON
    final_json = []
    for airline in airlines:
        airline_data = {
            "name": airline,
            "number_of_flights": [flight_count[(airline, date)] for date in dates],
            "negative_score": [final_exp[(airline, date)] for date in dates],
        }
        final_json.append(airline_data)

    # Save JSON file
    with open(output_json_path, "w") as outfile:
        json.dump(final_json, outfile)


# Example usage of the function
process_flight_data(
    "./DCAH_Competition_Data_VA_Flights.csv",
    "./data/final_results.csv",
    "./movingchart/updates.json",
)
