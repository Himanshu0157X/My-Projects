import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

def medi_buddy_chat():
    dataset_path = 'mini project/medicine_dataset copy.csv'
    print("Welcome to Medi-Buddy!")
    print("Type 'exit' to end the conversation.")
    df = pd.read_csv(dataset_path)

    if 'Condition' in df.columns:
        df['Symptoms'] = df['Symptoms'].apply(preprocess_text)
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df['Symptoms'])
        y = df['Condition']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
    else:
        print("Warning: The 'Condition' column is not present in the dataset. Personalized recommendations based on condition prediction will not be available.")
        rf_model = None

    patient_data = {
        'Name': [],
        'Age': [],
        'Gender': [],
        'BG': []
    }

    while True:
        patient_name = input("Please enter your name: ")
        track_user_interaction("User Input", patient_name)  

        if patient_name.lower() == 'exit':
            print("Goodbye!")
            break

        patient_age = input("Please enter your age: ")
        track_user_interaction("User Input", patient_age)

        if patient_age.lower() == 'exit':
            print("Goodbye!")
            break

        patient_gender = input("Please enter your gender: ")
        track_user_interaction("User Input", patient_gender)

        if patient_gender.lower() == 'exit':
            print("Goodbye!")
            break

        patient_BG = input("Blood Group: ")
        track_user_interaction("User Input", patient_BG)

        if patient_BG.lower() == 'exit':
            print("Goodbye!")
            break

        patient_data['Name'].append(patient_name)
        patient_data['Age'].append(patient_age)
        patient_data['Gender'].append(patient_gender)
        patient_data['BG'].append(patient_BG)

        user_input = input("Enter symptoms or a medical condition: ")
        track_user_interaction("User Input", user_input)

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        processed_input = preprocess_text(user_input)

        print("Medi-Buddy:")
        matching_rows = df[df['Symptoms'].str.contains(processed_input, case=False, na=False)]

        if not matching_rows.empty:
            print("Matching Symptoms:")
            print(matching_rows)

            if rf_model is not None:
                processed_input_vector = vectorizer.transform([processed_input])
                condition_prediction = rf_model.predict(processed_input_vector)
                predicted_condition = condition_prediction[0]

                personalized_recommendations = generate_recommendations(patient_age, patient_gender, predicted_condition)
                print("\nPersonalized Recommendations:")
                feedback = collect_feedback(personalized_recommendations)
                print("\nThank you for your feedback!")

                for recommendation, helpful in feedback:
                    track_recommendation_feedback(recommendation, helpful)
            else:
                personalized_recommendations = generate_recommendations(patient_age, patient_gender, None)
                print("\nRecommendations:")
                print("\n".join(personalized_recommendations))

            visualize_symptom_prevalence(df)

        else:
            print(f"No matching rows found for symptoms '{user_input}'.")
        ask_additional_question()

    patient_df = pd.DataFrame(patient_data)
    patient_df.to_csv('mini project/patient_data.csv', index=False)

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(tokens)

def generate_recommendations(age, gender, predicted_condition):
    recommendations = []
    if predicted_condition is not None:
        if predicted_condition == 'Diabetes':
            recommendations.append("Consider insulin therapy, dietary changes, and regular exercise.")
        elif predicted_condition == 'Heart Disease':
            recommendations.append("Adopt a healthy lifestyle, including a balanced diet and regular exercise.")
            recommendations.append("Your doctor may prescribe medications or suggest surgical interventions.")
        elif predicted_condition == 'Cancer':
            recommendations.append("Seek prompt medical attention for appropriate treatment, which may involve chemotherapy, radiation therapy, or surgery.")
        else:
            recommendations.append(f"The predicted condition is '{predicted_condition}'. Consult a doctor for further evaluation and personalized treatment recommendations.")
    else:
        recommendations.append("Consider consulting a doctor for further evaluation. Based on your symptoms, it's recommended to rest and stay hydrated. Avoid activities that worsen your symptoms.")

    return recommendations

def collect_feedback(recommendations):
    feedback = []
    for recommendation in recommendations:
        feedback_option = input(f"Was this recommendation helpful? [{recommendation}] (Yes/No): ")
        feedback.append((recommendation, feedback_option.lower() == 'yes'))
    return feedback

def visualize_symptom_prevalence(df):
    symptom_counts = df['Symptoms'].value_counts().nlargest(10)
    plt.figure(figsize=(10, 6))
    symptom_counts.plot(kind='bar')
    plt.title('Top 10 Symptom Prevalence')
    plt.xlabel('Symptoms')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()

def ask_additional_question():
    additional_question = input("Do you have any other symptoms or medical conditions to report? (Yes/No): ")
    track_user_interaction("Additional Question", additional_question)
    if additional_question.lower() == 'yes':
        user_input = input("Enter symptoms or a medical condition: ")
    elif additional_question.lower() == 'no':
        print("Thank you for using Medi-Buddy!")
    else:
        print("Invalid input. Please enter 'Yes' or 'No'.")

def track_user_interaction(interaction_type, interaction_data):
    pass

def track_recommendation_feedback(recommendation, helpful):
    pass

if __name__ == "__main__":
    medi_buddy_chat()