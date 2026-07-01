# Contributing

This project is small, but the code is split across multiple Tkinter windows, so changes should stay focused and easy to review.

## Before You Change Anything

- Read [README.md](README.md) and [WORKFLOW.md](WORKFLOW.md).
- Make sure your change matches the existing app flow.
- Avoid changing the behavior of unrelated windows unless the task requires it.

## Recommended Workflow

1. Create a branch for your change.
2. Make the smallest useful edit.
3. Test the specific part you changed.
4. Update documentation if the setup or flow changes.
5. Open a pull request with a short description of what changed and why.

## Code Style

- Keep the current Tkinter structure unless there is a clear reason to refactor.
- Use clear function and variable names.
- Prefer small, local changes over large rewrites.
- Do not hardcode secrets or machine-specific paths.

## Project-Specific Notes

- `main.py` is the launcher for the app.
- `studentV2f.py` handles student records and face sample capture.
- `trainV2f.py` trains the classifier from the `data/` folder.
- `face_detectorV2f.py` writes attendance to `attSheet.csv`.
- `attendenceV2f.py` is the CSV attendance viewer.

## Validation Expectations

If you change Python code, try to run a targeted check such as:

```powershell
python -m py_compile main.py studentV2f.py trainV2f.py face_detectorV2f.py attendenceV2f.py db_config.py
```

If you change the database flow, confirm the SQL script and `config.ini` still match the code.