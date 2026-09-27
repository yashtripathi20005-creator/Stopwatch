import tkinter as tk
from time import perf_counter


class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.after_id = None

        # Title
        title = tk.Label(
            root,
            text="STOPWATCH",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(25, 10))

        # Time display
        self.time_label = tk.Label(
            root,
            text="00:00:00.00",
            font=("Courier New", 36, "bold")
        )
        self.time_label.pack(pady=20)

        # Button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Start button
        self.start_button = tk.Button(
            button_frame,
            text="Start",
            width=10,
            font=("Arial", 12),
            command=self.start
        )
        self.start_button.grid(row=0, column=0, padx=5)

        # Stop button
        self.stop_button = tk.Button(
            button_frame,
            text="Stop",
            width=10,
            font=("Arial", 12),
            command=self.stop
        )
        self.stop_button.grid(row=0, column=1, padx=5)

        # Reset button
        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            width=10,
            font=("Arial", 12),
            command=self.reset
        )
        self.reset_button.grid(row=0, column=2, padx=5)

        # Lap button
        self.lap_button = tk.Button(
            root,
            text="Lap",
            width=10,
            font=("Arial", 12),
            command=self.lap
        )
        self.lap_button.pack(pady=5)

        # Lap display
        self.lap_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            justify="left"
        )
        self.lap_label.pack(pady=5)

        self.lap_count = 0

        # Close the application properly
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def format_time(self, seconds):
        """Convert seconds into HH:MM:SS.cc format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centiseconds = int((seconds * 100) % 100)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"

    def update_display(self):
        """Update the stopwatch display."""
        if self.running:
            current_time = perf_counter()
            elapsed = self.elapsed_time + (current_time - self.start_time)

            self.time_label.config(
                text=self.format_time(elapsed)
            )

            self.after_id = self.root.after(10, self.update_display)

    def start(self):
        """Start or resume the stopwatch."""
        if not self.running:
            self.running = True
            self.start_time = perf_counter()

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            self.update_display()

    def stop(self):
        """Stop/pause the stopwatch."""
        if self.running:
            current_time = perf_counter()
            self.elapsed_time += current_time - self.start_time

            self.running = False

            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

            self.time_label.config(
                text=self.format_time(self.elapsed_time)
            )

            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def reset(self):
        """Reset the stopwatch to zero."""
        self.running = False
        self.elapsed_time = 0
        self.start_time = 0
        self.lap_count = 0

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.time_label.config(text="00:00:00.00")
        self.lap_label.config(text="")

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    def lap(self):
        """Record the current stopwatch time."""
        if self.running or self.elapsed_time > 0:
            if self.running:
                current_time = perf_counter()
                current_elapsed = (
                    self.elapsed_time +
                    (current_time - self.start_time)
                )
            else:
                current_elapsed = self.elapsed_time

            self.lap_count += 1

            lap_text = (
                f"Lap {self.lap_count}: "
                f"{self.format_time(current_elapsed)}"
            )

            current_text = self.lap_label.cget("text")

            if current_text:
                current_text += "\n" + lap_text
            else:
                current_text = lap_text

            self.lap_label.config(text=current_text)

    def close(self):
        """Close the application."""
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)

        self.root.destroy()


def main():
    root = tk.Tk()
    Stopwatch(root)
    root.mainloop()


if __name__ == "__main__":
    main()
