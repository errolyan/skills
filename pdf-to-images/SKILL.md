---
name: pdf-to-images
description: Convert PDF pages to PNG images. Use this skill when the user wants to convert PDFs to images, extract PDF pages as images, create screenshots/previews from PDFs, or needs PDF content as image files for any purpose (presentations, web, processing). Triggers on phrases like "PDF to images", "convert PDF to PNG", "extract PDF pages", "PDF screenshots", or when the user needs to process PDF content as images.
---

# PDF to Images Converter

This skill converts each page of a PDF file into a separate PNG image at high quality (300 DPI).

## When to Use This Skill

Use this skill whenever the user wants to:
- Convert PDF pages to image files
- Extract individual pages from a PDF as images
- Create image previews or screenshots from PDFs
- Process PDF content in image format for presentations, websites, or other uses
- Split a PDF into page images

## How It Works

The skill uses the `pdf2image` Python library (which requires `poppler` system tools) to render each PDF page as a high-quality PNG image.

### Dependencies

This skill requires:
- Python package: `pdf2image`
- System tool: `poppler` (provides `pdftoppm`)

Check and install dependencies before running:

```bash
# Check if poppler is installed
which pdftoppm || echo "Need to install poppler"

# Install poppler (macOS)
brew install poppler

# Install poppler (Ubuntu/Debian)
sudo apt-get install poppler-utils

# Install pdf2image Python package
pip3 install pdf2image
```

## Usage Pattern

When the user asks to convert PDFs to images:

1. **Identify the PDF file(s)**
   - Ask for the PDF file path if not provided
   - Use Glob to find PDFs if the user gives a directory
   - Verify the file exists before proceeding

2. **Determine output location**
   - Ask where to save images if not specified
   - Default: create an `output_images/` directory in the current location
   - For multiple PDFs: create subdirectories named after each PDF

3. **Check dependencies**
   - Verify `poppler` is installed (`which pdftoppm`)
   - Install if missing (offer to install via brew/apt)
   - Verify `pdf2image` Python package is available
   - Install if missing (`pip3 install pdf2image`)

4. **Run the conversion script**
   - Use the bundled `convert_pdf.py` script in the `scripts/` directory
   - Pass parameters: PDF path, output directory, and DPI (default 300)

5. **Report results**
   - Tell the user how many pages were converted
   - Show the output directory path
   - Report file sizes if relevant

## The Conversion Script

Use the bundled script at `scripts/convert_pdf.py`:

```bash
python3 <skill-path>/scripts/convert_pdf.py \
  --pdf <pdf-file-path> \
  --output <output-directory> \
  --dpi 300
```

Parameters:
- `--pdf`: Path to the PDF file (required)
- `--output`: Output directory path (required)
- `--dpi`: Resolution in DPI (default: 300, range: 150-600)

The script will:
- Create the output directory if it doesn't exist
- Convert each page to a PNG image named `page_001.png`, `page_002.png`, etc.
- Print progress for each page
- Report total pages converted and output location

## Example Workflows

### Single PDF conversion
```
User: "Convert document.pdf to images"

1. Check if poppler installed
2. Install dependencies if needed
3. Run: python3 scripts/convert_pdf.py --pdf document.pdf --output ./output_images
4. Report: "Converted 15 pages to ./output_images/"
```

### Multiple PDFs
```
User: "Convert all PDFs in ./reports to images"

1. Find all PDFs: glob "reports/*.pdf"
2. Check dependencies
3. For each PDF, create subdirectory and convert
4. Report total pages converted
```

### Custom output location
```
User: "Extract pages from thesis.pdf and save to ~/Desktop/thesis_pages"

1. Check dependencies
2. Run with custom output path
3. Verify results and report
```

## Quality Settings

Default DPI is 300 (high quality, suitable for most uses):
- **150 DPI**: Lower quality, smaller files (web previews)
- **300 DPI**: Standard quality (default, recommended)
- **600 DPI**: High quality, larger files (print quality)

Only change DPI if the user specifically requests higher/lower quality.

## Error Handling

Common issues and solutions:

**"Unable to get page count. Is poppler installed?"**
- Poppler is not installed or not in PATH
- Solution: Install poppler via package manager

**"ModuleNotFoundError: No module named 'pdf2image'"**
- Python package not installed
- Solution: `pip3 install pdf2image`

**"FileNotFoundError" or "No such file"**
- PDF path is incorrect
- Solution: Verify file exists, use absolute paths

**"Permission denied"**
- Cannot write to output directory
- Solution: Check directory permissions or choose different location

## Output Organization

For single PDF:
```
output_directory/
├── page_001.png
├── page_002.png
├── page_003.png
└── ...
```

For multiple PDFs:
```
output_directory/
├── document1/
│   ├── page_001.png
│   └── page_002.png
├── document2/
│   ├── page_001.png
│   └── page_002.png
└── ...
```

## Important Notes

- Always check and install dependencies before attempting conversion
- PNG format is used for lossless quality (no JPEG artifacts)
- Image file sizes depend on page complexity and DPI setting
- Processing large PDFs (100+ pages) may take several minutes
- The skill preserves page order exactly as in the PDF
