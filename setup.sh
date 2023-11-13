python -m venv venv

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source env/bin/activate
elif [[ "$OSTYPE" == "msys"* ]]; then
    source env/Scripts/activate
else
    echo "Système d'exploitation non pris en charge."
    exit 1
fi

# Installer les dépendances
pip install -r requirements.txt