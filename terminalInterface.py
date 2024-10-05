from rich.console import Console
from rich.table import Table
import time

class Dashboard:
    def __init__(self):
        self.console = Console()
        self.stats = {}
        self.logs = []

    def update_stats(self, new_stats):
        """Update the stats dictionary."""
        self.stats = new_stats
    
    def update_logs(self, new_logs):
        self.logs = new_logs
        self.logs = self.logs[-15:]

    def add_log(self, log_entry):
        """Add a new log entry to the logs list."""
        self.logs.append(log_entry)
        # Keep only the last 10 logs
        self.logs = self.logs[-10:]

    def display(self):
        """Display the dashboard with stats and logs."""
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Stats", width=30)
        table.add_column("Logs", width=100)

        # Determine the number of rows needed (max between logs and stats length)
        max_rows = max(len(self.stats), len(self.logs))

        # Add rows with stats on the left and logs on the right
        for i in range(max_rows):
            stat_entry = ""
            log_entry = ""

            # Add stats entries
            if i < len(self.stats):
                key = list(self.stats.keys())[i]
                value = self.stats[key]
                stat_entry = f"{key}: {value}"

            # Add log entries
            if i < len(self.logs):
                log_entry = self.logs[i]

            table.add_row(stat_entry, log_entry)

        # Clear the console and print the table
        self.console.clear()
        self.console.print(table)

# if __name__ == "__main__":
#     dashboard = Dashboard()

#     # Simulate updating stats and logs
#     try:
#         for i in range(1, 21):  # Simulate 20 updates
#             # Update stats
#             new_stats = {
#                 "Process A": i * 2,
#                 "Process B": i * 3,
#                 "Process C": i * 5
#             }
#             dashboard.update_stats(new_stats)

#             # Add a log entry
#             dashboard.add_log(f"Log entry {i}: Processed event {i}")

#             # Display the dashboard
#             dashboard.display()

#             # Sleep to simulate time between updates
#             time.sleep(1)

#     except KeyboardInterrupt:
#         print("Terminated by user.")