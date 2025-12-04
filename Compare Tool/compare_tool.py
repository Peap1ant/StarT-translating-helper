import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class JsonComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON Comparator (Analysis Tool)")
        self.root.geometry("550x200")
        self.root.resizable(False, False)

        # Initialize variables
        self.source_path = tk.StringVar()
        self.target_path = tk.StringVar()

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Area
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # --- Original (Source) File ---
        lbl_source = tk.Label(input_frame, text="Original JSON:", width=12, anchor="w", font=("Arial", 10, "bold"))
        lbl_source.grid(row=0, column=0, pady=5)

        entry_source = tk.Entry(input_frame, textvariable=self.source_path, width=45)
        entry_source.grid(row=0, column=1, padx=5, pady=5)

        btn_source = tk.Button(input_frame, text="Browse", command=self.select_source, width=10)
        btn_source.grid(row=0, column=2, padx=5, pady=5)

        # --- Target File ---
        lbl_target = tk.Label(input_frame, text="Target JSON:", width=12, anchor="w", font=("Arial", 10, "bold"))
        lbl_target.grid(row=1, column=0, pady=5)

        entry_target = tk.Entry(input_frame, textvariable=self.target_path, width=45)
        entry_target.grid(row=1, column=1, padx=5, pady=5)

        btn_target = tk.Button(input_frame, text="Browse", command=self.select_target, width=10)
        btn_target.grid(row=1, column=2, padx=5, pady=5)

        # Action Button
        btn_compare = tk.Button(main_frame, text="Compare JSON Files", 
                            command=self.compare_json, bg="#ffcccb", height=2, font=("Arial", 11, "bold"))
        btn_compare.pack(fill=tk.X)

    def select_source(self):
        filename = filedialog.askopenfilename(title="Select Original JSON", filetypes=[("JSON files", "*.json")])
        if filename:
            self.source_path.set(filename)

    def select_target(self):
        filename = filedialog.askopenfilename(title="Select Target JSON", filetypes=[("JSON files", "*.json")])
        if filename:
            self.target_path.set(filename)

    def compare_json(self):
        s_path = self.source_path.get()
        t_path = self.target_path.get()

        if not s_path or not t_path:
            messagebox.showwarning("Warning", "Please select both Original and Target files.")
            return

        try:
            # Read Files
            with open(s_path, "r", encoding="utf-8") as f:
                source_data = json.load(f)
            
            with open(t_path, "r", encoding="utf-8") as f:
                target_data = json.load(f)

            if not isinstance(source_data, dict) or not isinstance(target_data, dict):
                messagebox.showerror("Error", "Top-level structure must be a Dictionary (Object).")
                return

            # Analyze Logic
            # A. Keys in Target but NOT in Original (New Keys)
            new_keys_in_target = [key for key in target_data.keys() if key not in source_data]

            # B. Keys in BOTH but values are different (Changed Keys)
            changed_value_keys = []
            for key in source_data.keys():
                if key in target_data:
                    if source_data[key] != target_data[key]:
                        changed_value_keys.append(key)

            # 3. Output - Console
            print("\n" + "="*40)
            print(" [Comparison Result]")
            print("="*40)
            
            print(f"\n1. Keys in Target but NOT in Original (New Keys): {len(new_keys_in_target)}")
            for k in new_keys_in_target:
                print(f" - {k}")

            print(f"\n2. Keys with Different Values (Changed Keys): {len(changed_value_keys)}")
            for k in changed_value_keys:
                print(f" - {k}")
            print("\n" + "="*40 + "\n")

            # Output - TXT File
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_txt_path = os.path.join(script_dir, "compare_key.txt")

            with open(output_txt_path, "w", encoding="utf-8") as f:
                # New keys
                f.write(f"new keys (Total: {len(new_keys_in_target)}):\n")
                for k in new_keys_in_target:
                    f.write(f'"{k}"\n')
                
                f.write("\n---\n\n")

                f.write(f"changed keys (Total: {len(changed_value_keys)}):\n")
                for k in changed_value_keys:
                    f.write(f'"{k}"\n')

            # Output - GUI Messagebox
            msg = f"Comparison Complete!\n\n"
            msg += f"[New Keys Count]: {len(new_keys_in_target)}\n"
            msg += f"(Keys in Target but not in Original)\n\n"
            msg += f"[Changed Keys Count]: {len(changed_value_keys)}\n"
            msg += f"(Keys with different values)\n\n"
            msg += f"Report saved to:\n{output_txt_path}"

            messagebox.showinfo("Result", msg)

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JsonComparatorApp(root)
    root.mainloop()
