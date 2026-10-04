# Presentify

Turn a research paper into a PowerPoint presentation. This prototype extracts text from an uploaded PDF or arXiv paper, organizes it into academic sections using Gemini, and generates a `.pptx` slide deck.

[Watch the demo](https://youtu.be/pY7fP9XLudg) · [Portfolio](https://atulshreewastav.com.np/#projects)

## How it works

1. Upload a PDF (up to 12 MB) or provide an arXiv abstract URL.
2. Extract and clean the paper text.
3. Use Gemini to extract introduction, literature review, methodology, results, and conclusions.
4. Generate a title slide and section slides with `python-pptx`.

The repository also contains a T5-based summarization module. The current slide-generation endpoint uses the Gemini-extracted sections directly.

## Repository guide

| File | Purpose |
| --- | --- |
| `app.py` | FastAPI endpoints and presentation workflow |
| `pdftools.py` | PDF text extraction and cleanup |
| `gemini.py` | Section extraction with Gemini |
| `presentify_model.py` | Hugging Face summarization module |
| `pptxtools.py` | PowerPoint formatting helpers |
| `FrontEnd/` | HTML, CSS, and JavaScript frontend |

## Local development

This is an older prototype, not a maintained production service. Its pinned dependencies include Windows-only `pywin32`, and it uses the legacy `google-generativeai` SDK and `gemini-pro` model. Update the provider integration and resolve platform dependencies before expecting a working end-to-end run. [Google SDK migration guide](https://ai.google.dev/gemini-api/docs/migrate).

After resolving those prerequisites, the backend entry point is:

```bash
python -m venv .venv
# Activate the virtual environment for your shell.
python -m pip install -r requirements.txt
mkdir -p slides
export GOOGLE_API_KEY="your-own-key"
python -m uvicorn app:app --reload
```

The summarization model `atulxop/deployment_model` is loaded at startup and requires access to its Hugging Face files. Open `http://127.0.0.1:8000/docs` to inspect the API. Generated presentations are saved under `slides/`.

## API workflow

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/extract-text` | Upload a PDF |
| POST | `/get_data_from_url` | Load an arXiv paper via `arxiv_url` query parameter |
| GET | `/get-section-data` | Extract sections from the loaded paper |
| GET | `/generate_slide` | Write a PowerPoint presentation |

Load a paper before extracting sections, then generate the slides. The prototype uses shared in-memory state and a shared temporary PDF, so it is intended for single-user local exploration. Review generated content against the original paper.

## Example output

Slides generated from *Attention Is All You Need*:

![Example slide 1](https://github.com/AtuLxCE/PresentifyWebapp/assets/81093679/c45c8019-d417-4c72-a061-3f14061be37c)

![Example slide 2](https://github.com/AtuLxCE/PresentifyWebapp/assets/81093679/b9e63b12-ebe7-4ab4-8794-215af26c3c9f)

![Example slide 3](https://github.com/AtuLxCE/PresentifyWebapp/assets/81093679/8b0ab74e-9695-475a-aab4-047052efefdb)

## License

See [LICENSE](LICENSE).
