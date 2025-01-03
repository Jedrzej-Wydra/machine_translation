import subprocess
import sys

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

def install_spacy_model(model):
    """Download a SpaCy model."""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model])
        print(f"Successfully downloaded SpaCy model: {model}")
    except subprocess.CalledProcessError:
        print(f"Failed to download SpaCy model: {model}")

# List of required packages
packages = ["spacy", "re", "openai", "markdown", "os"]

# Install each package
for package in packages:
    install_package(package)

# Install the SpaCy model
install_spacy_model("xx_ent_wiki_sm")