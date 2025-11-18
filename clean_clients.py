import sys
import pandas as pd

from dateutil import parser


def normalize_name(name):
    if not isinstance(name, str):
        return name
    return name.strip().title()


def normalize_phone(phone):
    if not isinstance(phone, str):
        return None

    digits = "".join(ch for ch in phone if ch.isdigit())

    if len(digits) == 10:
        return "+1" + digits
    elif len(digits) == 11 and digits.startswith("1"):
        return "+" + digits
    else:
        return None


def normalize_dates(df, column):
    if column not in df.columns:
        return df

    df = df.copy()

    def parse_date(x):
        try:
            return parser.parse(str(x), dayfirst=False)
        except:
            return None   # don't drop, just return None

    df[column] = df[column].apply(parse_date)

    # Format all valid dates, leave invalid ones as None
    df[column] = df[column].apply(
        lambda d: d.strftime("%Y-%m-%d") if pd.notnull(d) else None
    )

    return df


def clean_dataframe(df):
    # Remove rows with missing client_id or email
    df = df.dropna(subset=["client_id", "email"]).copy()

    # Normalize names
    if "first_name" in df.columns:
        df["first_name"] = df["first_name"].apply(normalize_name)
    if "last_name" in df.columns:
        df["last_name"] = df["last_name"].apply(normalize_name)

    # Normalize phone numbers
    if "phone" in df.columns:
        df["phone"] = df["phone"].apply(normalize_phone)

    # Normalize join_date
    df = normalize_dates(df, "join_date")

    # Deduplicate based on client_id
    df = df.sort_values("client_id")
    df = df.drop_duplicates(subset=["client_id"], keep="first")

    return df


def load_csv(path):
    return pd.read_csv(path)


def save_csv(df, path):
    df.to_csv(path, index=False)


def main():
    try:
        df_raw = load_csv("clients_raw.csv")
    except Exception as e:
        print(f'Error reading input file: {e}')
        sys.exit(1)

    print(df_raw.to_string())

    try:
        df_clean = clean_dataframe(df_raw)
    except Exception as e:
        print(f"Error cleaning data: {e}")
        sys.exit(1)

    print(df_clean.to_string())

    try:
        save_csv(df_clean, "clients_clean.csv")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()