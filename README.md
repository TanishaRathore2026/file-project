# 📁 FileHub — File Manager

A simple CRUD file-handling app built with **Python** and **Streamlit**. Create, read, update, rename, and delete text files right from your browser.

## Features
- ✨ Create new files with custom content
- 👁️ Read and preview file contents (with download option)
- ✏️ Update files — append, overwrite, or rename
- 🗑️ Delete files with confirmation
- 📂 Live sidebar file explorer with size info

## Tech Stack
- Python
- Streamlit
- `pathlib` for file handling

## Getting Started

```bash

# Install dependencies
pip install streamlit

# Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## Project Structure
```
filehub/
├── app.py          # Streamlit UI
└── storage/         # Files created via the app (auto-generated)
```


## License
Tanisha Rathore
