import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# List of city, month and day options
cities = ["chicago", "new york city", "washington"]
months = ["January", "February", "March", "April", "May", "June", "All"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "All"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like to see data for Chicago, New York City, or Washington: ").lower()
        if city not in cities:
            print("Oops, please enter a valid city.")
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input("If you would like to filter for a specific month, please input a month between January and June. Otherwise type All: ").title()
        if month not in months:
            print("Oops, please enter a valid month.")
        else:
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("If you would like to filter by day, please input the specific day of the week (eg. Monday). Otherwise type All: ").title()
        if day not in days:
            print("Please enter a valid day of the week.")
        else:
            break

    response = "\nThank you for selecting {} for city, {} for month, and {} for day. Calculating relevant statistics..."
    print(response.format(city.title(), month, day))
    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city])

    # CREATE: additional columns needed
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # extract day of week from the Start Time column to create a day of week column
    df['day of week'] = df['Start Time'].dt.weekday_name
    # extract hour from Start Time column to create hour column
    df['hour'] = df['Start Time'].dt.hour
    # combine columns to create a Start & End Station column
    df['Start & End Station'] = df['Start Station'] + " to " + df['Start Station']


    if month != 'All':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day of week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_name = months[popular_month - 1]
    print('Most Common Month:', popular_month_name)

    # TO DO: display the most common day of week
    common_day = df['day of week'].mode()[0]
    print('Most Common Day:', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Used Start Station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Used End Station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    common_startend_station = df['Start & End Station'].mode()[0]
    print('Most Used Station Combination:', common_startend_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time (converting seconds to hours)
    total_time = df['Trip Duration'].sum() / 360
    print('Total Travel Time:', int(total_time), 'hours')


    # TO DO: display mean travel time (converting seconds to hours)
    avg_time = df['Trip Duration'].mean() / 360
    print('Average Travel Time:', avg_time.round(1), 'hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types and Counts:\n',user_types)

    # TO DO: Display counts of gender
    if 'Gender' not in df:
        print('\nSorry, there is no gender data for this selection.')
    else:
        gender_counts = df['Gender'].fillna('Not Listed').value_counts()
        print('\nGender and Counts:\n',gender_counts)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df:
        print('\nSorry, there is no birth year data for this selection.')
    else:
        min_year = df['Birth Year'].dropna(axis = 0).astype(int).min()
        max_year = df['Birth Year'].dropna(axis = 0).astype(int).max()
        common_year = df['Birth Year'].dropna(axis = 0).astype(int).mode()[0]
        print('\nYear Information', '\n Earliest Birth Year:', min_year, '\n Most Recent Birth Year:', max_year, '\n Most Common Birth Year:', common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    """Displays raw data."""
    # Asks user if they want to view the data and continues until they input no.
    show_data = input('\nWould you like to see 5 lines of raw data? ').lower()
    start_loc = 0
    while show_data != 'no':
        if show_data != 'yes':
            show_data = input('\nPlease type "yes" or "no". ').lower()
        else:
            pd.set_option('display.max_columns', 20)
            print(df.iloc[start_loc : start_loc + 5])
            start_loc += 5
            show_data = input('\nWould you like to see 5 more lines of data? ').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
