import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class MediBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medi-Buddy")
        
        # Variables to store user input
        self.patient_name = tk.StringVar()
        self.patient_age = tk.StringVar()
        self.patient_gender = tk.StringVar()
        self.patient_bg = tk.StringVar()
        self.user_input = tk.StringVar()

        # Frame for user input
        input_frame = ttk.Frame(self.root)
        input_frame.pack(padx=20, pady=20)

        # Labels and entry widgets for user input
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.patient_name).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.patient_age).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Combobox(input_frame, textvariable=self.patient_gender, values=["Male", "Female", "Other"]).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Blood Group:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.patient_bg).grid(row=3, column=1, padx=5, pady=5)

        # Entry widget for symptoms or medical conditions
        ttk.Label(input_frame, text="Symptoms or Medical Conditions:").grid(row=4, column=0, padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.user_input).grid(row=4, column=1, padx=5, pady=5)

        # Button to submit user input
        ttk.Button(input_frame, text="Submit", command=self.submit_input).grid(row=5, columnspan=2, pady=10)

    def submit_input(self):
        # Retrieve user input
        name = self.patient_name.get()
        age = self.patient_age.get()
        gender = self.patient_gender.get()
        bg = self.patient_bg.get()
        user_input = self.user_input.get()

        # Perform processing (similar to your existing code)
        processed_input = preprocess_text(user_input)
        matching_rows = df[df['Symptoms'].str.contains(processed_input, case=False, na=False)]

        # Display output
        if not matching_rows.empty:
            messagebox.showinfo("Matching Symptoms", matching_rows.to_string(index=False))
        else:
            messagebox.showinfo("No Matching Symptoms", f"No matching rows found for symptoms '{user_input}'.")

        # Clear input fields
        self.patient_name.set('')
        self.patient_age.set('')
        self.patient_gender.set('')
        self.patient_bg.set('')
        self.user_input.set('')

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(tokens)

# Load dataset
dataset_path = 'mini project/medicine_dataset copy.csv'
df = pd.read_csv(dataset_path)

# Create Tkinter window and run the app
root = tk.Tk()
app = MediBuddyApp(root)
root.mainloop()
 