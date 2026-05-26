# Doclira PDF Lite

**Free, open-source PDF basics for Windows. Process files locally on your computer.**

[Official Website](https://www.doclira.com/) | [Doclira PDF Pro](https://taixianglumark.gumroad.com/l/doclira-pdf) | [User Guide](https://www.doclira.com/guide/)

Doclira PDF Lite is a small desktop application for everyday page-level PDF work.
It is deliberately focused: useful enough for simple tasks, while advanced business
workflows remain in the commercial Doclira PDF Pro edition.

## Included In Lite

- Open and preview a PDF locally
- Merge multiple PDF files
- Split a PDF into individual page files
- Rotate one page and save a new copy
- Remove one page and save a new copy
- Add a basic single-file footer text watermark

## Lite And Pro

| Capability | Lite | Doclira PDF Pro |
| --- | :---: | :---: |
| Local PDF preview | Yes | Yes |
| Merge, split, rotate and delete pages | Yes | Yes |
| Basic single-file text watermark | Yes | Yes |
| Batch processing and visible file queue | - | Yes |
| Tiled, logo, opacity and page-range watermark workflows | - | Yes |
| PDF to Word and image conversion tools | - | Yes |
| Lightweight PDF text correction interface | - | Yes |
| Commercial Windows installer and support | - | Yes |

For the full Windows product, examples and purchase delivery, visit
[www.doclira.com](https://www.doclira.com/).

## Run From Source

Requirements:

- Windows 10 or Windows 11
- Python 3.10 or newer, 64-bit recommended

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python run.py
```

## Privacy

PDF processing runs locally. Lite does not upload your PDF files to Doclira servers.
Do not attach confidential documents when opening a public GitHub issue.

## Project Scope

This repository contains only the free Lite implementation. It does not contain
Doclira PDF Pro source code, license handling, paid installer files or advanced
commercial workflow implementations.

## Support

- Lite issues and feature requests: use [GitHub Issues](https://github.com/lienowen/doclira-pdf-lite/issues)
- Product and purchasing questions: [www.doclira.com](https://www.doclira.com/)

## License

Doclira PDF Lite is released under the MIT License. Doclira PDF Pro is a separate
commercial product and is not licensed through this repository.

The Doclira name and product branding identify the official product and are not
granted for reuse by the MIT license.
