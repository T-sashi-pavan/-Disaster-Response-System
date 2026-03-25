

import os
import re
import pickle
import nltk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

nltk.download(['punkt', 'wordnet'])


def tokenize(text):
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(tok) for tok in tokens]


def load_data(msg_path, cat_path):
    messages = pd.read_csv(msg_path)
    categories = pd.read_csv(cat_path)

    df = messages.merge(categories, on="id")
    cats = df["categories"].str.split(";", expand=True)
    cats.columns = [c[:-2] for c in cats.iloc[0]]

    for col in cats:
        cats[col] = cats[col].str[-1].astype(int)

    df.drop("categories", axis=1, inplace=True)
    df = pd.concat([df, cats], axis=1)
    df = df[df["related"] != 2]

    return df["message"], df.iloc[:, 4:]


def get_valid_labels(y):
    return [col for col in y.columns if y[col].nunique() > 1]


def get_models():
    return {
        "LogisticRegression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            n_jobs=-1
        ),
        "LinearSVM": LinearSVC(
            class_weight="balanced"
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=400,
            max_depth=25,
            min_samples_split=5,
            class_weight="balanced_subsample",
            n_jobs=-1,
           random_state=42
        ),
        "SGDClassifier": SGDClassifier(
            loss="log_loss",
            class_weight="balanced",
            max_iter=2000,
            random_state=42
        )
    }

def train_model(name, clf, X_train, X_test, y_train, y_test):
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(tokenizer=tokenize, max_features=12000,ngram_range=(1, 2))),
        ("clf", MultiOutputClassifier(clf))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "micro_f1": f1_score(y_test, preds, average="micro"),
        "macro_f1": f1_score(y_test, preds, average="macro")
    }

    print(f"{name} → Micro-F1: {metrics['micro_f1']:.3f}")
    return pipeline, metrics

def save_graphs(results_df, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    # Accuracy graph
    plt.figure(figsize=(8, 5))
    plt.bar(results_df["Model"], results_df["Accuracy"])
    plt.title("Model Accuracy Comparison")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "model_accuracy_comparison.png"))
    plt.close()

    # F1 graph
    plt.figure(figsize=(8, 5))
    plt.bar(results_df["Model"], results_df["Micro F1"])
    plt.title("Model F1 Score Comparison")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "model_f1_comparison.png"))
    plt.close()


def main():
    BASE = r"C:\Users\DELL\PycharmProjects\DisasterResponse\.venv\New_DisasterResponseTweets_2026"
    MESSAGES = os.path.join(BASE, "Dataset/disaster_messages.csv")
    CATEGORIES = os.path.join(BASE, "Dataset/disaster_categories.csv")
    MODEL_PATH = os.path.join(BASE, "ModelFiles/disaster_model.pkl")
    REPORT_DIR = os.path.join(BASE, "Reports")

    X, y = load_data(MESSAGES, CATEGORIES)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = []
    best_model = None
    best_score = 0
    best_name = ""

    valid_labels = get_valid_labels(y_train)

    y_train_valid = y_train[valid_labels]
    y_test_valid = y_test[valid_labels]

    removed_labels = set(y.columns) - set(valid_labels)
    print(f"⚠ Removed single-class labels: {removed_labels}")

    for name, clf in get_models().items():
        model, metrics = train_model(
            name,
            clf,
            X_train,
            X_test,
            y_train_valid,
            y_test_valid
        )

        results.append({
            "Model": name,
            "Accuracy": metrics["accuracy"],
            "Micro F1": metrics["micro_f1"],
            "Macro F1": metrics["macro_f1"]
        })

        if metrics["micro_f1"] > best_score:
            best_score = metrics["micro_f1"]
            best_model = model
            best_name = name

    results_df = pd.DataFrame(results)
    print("\nFinal Comparison:\n", results_df)

    save_graphs(results_df, REPORT_DIR)

    payload = {
        "model": best_model,
        "labels": valid_labels,
        "best_model": best_name
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(payload, f)

    print(f"\n✅ Best Model Saved: {best_name}")

if __name__ == "__main__":
    main()
