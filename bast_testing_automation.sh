. .venv/Scripts/activate

python -m app.py
python -m pytest test.py

PYTEST_EXIT_CODE=$?


if [ $PYTEST_EXIT_CODE -eq 0 ]
then 
   exit 0
else
   exit 1
fi