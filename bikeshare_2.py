import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}

MONTHS = ["january", "february", "march", "april", "may", "june"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            "Which city would you like to explore: Chicago, New York City, or Washington?\n"
        ).lower()
        if city in CITY_DATA:
            break
        else:
            print(
                "Invalid input. Please choose from Chicago, New York City, or Washington."
            )

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Which month would you like to explore? (all, january, february, ..., june)\n"
        ).lower()
        if month in ["all"] + MONTHS:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Which day would you like to explore? (all, monday, tuesday, ... sunday)\n"
        ).lower()
        if day in [
            "all",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]:
            break
        else:
            print("Invalid input. Please enter a valid day or 'all'.")

    print("-" * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # Filter by month if applicable
    if month != "all":
        # Use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df["month"] == month]

    # Filter by day of week if applicable
    if day != "all":
        # Filter by day of week to create the new dataframe
        df = df[df["day_of_week"].str.lower() == day.lower()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # Display the most common month
    common_month = df["month"].mode()[0]
    print(f"The most common month is: {common_month}")

    # Display the most common day of week
    common_day = df["day_of_week"].mode()[0]
    print(f"The most common day of week is: {common_day}")

    # Display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print(f"The most common start hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df["Trip"] = df["Start Station"] + " to " + df["End Station"]
    common_trip = df["Trip"].mode()[0]
    print(f"The most frequent trip is from {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print(f"Total travel time: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("User Type counts:")
    print(user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        gender_counts = df["Gender"].value_counts()
        print("\nGender counts:")
        print(gender_counts)
    else:
        print("\nGender data not available.")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_birth = df["Birth Year"].min()
        most_recent_birth = df["Birth Year"].max()
        most_common_birth = df["Birth Year"].mode()[0]
        print("\nBirth Year statistics:")
        print(f"Earliest birth year: {earliest_birth}")
        print(f"Most recent birth year: {most_recent_birth}")
        print(f"Most common birth year: {most_common_birth}")
    else:
        print("\nBirth year data not available.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_raw_data(df):
    start_row = 0
    display_more = input(
        "Do you want to check the first 5 rows of the dataset related to the chosen city? (yes/no)\n"
    ).lower()

    while display_more == "yes":
        print(df.iloc[start_row : start_row + 5])
        start_row += 5

        if start_row >= len(df):
            print("No more data to display.")
            break

        display_more = input(
            "Do you want to check another 5 rows of the dataset? (yes/no)\n"
        ).lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
