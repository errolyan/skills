#!/usr/bin/env python3
"""
Convert PDF pages to PNG images

Usage:
    python convert_pdf.py --pdf <pdf-file> --output <output-dir> [--dpi <dpi>]
"""

import argparse
import os
import sys
from pathlib import Path


def convert_pdf_to_images(pdf_path, output_dir, dpi=300):
    """
    Convert each page of a PDF to a separate PNG image.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the images
        dpi: Resolution in DPI (default: 300)

    Returns:
        Number of pages converted
    """
    try:
        from pdf2image import convert_from_path
    except ImportError:
        print("Error: pdf2image is not installed.")
        print("Install it with: pip3 install pdf2image")
        sys.exit(1)

    # Verify PDF exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print(f"Converting: {pdf_path}")
    print(f"Output directory: {output_dir}")
    print(f"Resolution: {dpi} DPI")
    print()

    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)

        # Save each page
        for i, image in enumerate(images, start=1):
            output_path = os.path.join(output_dir, f'page_{i:03d}.png')
            image.save(output_path, 'PNG')
            print(f"  ✓ Saved: page_{i:03d}.png")

        print()
        print(f"Success! Converted {len(images)} pages")
        print(f"Images saved to: {output_dir}")

        return len(images)

    except Exception as e:
        print(f"Error during conversion: {e}")

        # Provide helpful error messages
        if "poppler" in str(e).lower():
            print()
            print("Poppler is not installed or not in PATH.")
            print("Install it with:")
            print("  macOS:        brew install poppler")
            print("  Ubuntu/Debian: sudo apt-get install poppler-utils")

        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF pages to PNG images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pdf document.pdf --output ./images
  %(prog)s --pdf report.pdf --output ~/Desktop/report_pages --dpi 600
        """
    )

    parser.add_argument(
        '--pdf',
        required=True,
        help='Path to the PDF file'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Output directory for the images'
    )

    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='Resolution in DPI (default: 300, range: 150-600)'
    )

    args = parser.parse_args()

    # Validate DPI range
    if not 150 <= args.dpi <= 600:
        print("Warning: DPI should be between 150 and 600")
        print(f"Using DPI={args.dpi} anyway...")

    # Run conversion
    convert_pdf_to_images(args.pdf, args.output, args.dpi)


if __name__ == '__main__':
    main()
