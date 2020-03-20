import os
import datetime

def get_path(session_data):
    provider_path = "./data_output" + "/" + session_data["provider"].replace("-", "_")
    transformation_dates = []
    if os.path.isdir(provider_path):
        for date in os.listdir(provider_path):
            if date.startswith(
                    "2"):  # Workaround, um nur relevante Ordner einzuschließen (schließt insbesondere unsichtbare Ordner auf Unix-Systemen aus, die mit einem "." beginnen)
                transformation_dates.append(date)
        if len(transformation_dates) > 0:
            transformation_date = max(transformation_dates, key=lambda d: datetime.datetime.strptime(d, "%Y%m%d"))
            output_path = provider_path + "/" + transformation_date
        else:
            output_path = "no_provider_data"
    else:
        output_path = "no_provider_data"

    return output_path
