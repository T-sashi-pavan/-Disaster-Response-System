import nltk

# Download all required NLTK resources
resources = ['punkt_tab', 'wordnet', 'averaged_perceptron_tagger', 'omw-1.4']

for resource in resources:
    print(f"Downloading {resource}...")
    nltk.download(resource, quiet=True)

print("All NLTK resources downloaded successfully!")