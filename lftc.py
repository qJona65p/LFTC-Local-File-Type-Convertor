import sys
import os
from pathlib import Path
import fitz

def pdf_to_png(pdf_path: str, output_dir: str = None, dpi: int = 300):
    if output_dir is None:
        output_dir = pdf_path + "_pages"
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    print(f"Converting {len(doc)} pages from {pdf_path}...")

    for i, page in enumerate(doc):
        # Higher dpi = better quality (but larger files). 300 is usually excellent.
        pix = page.get_pixmap(dpi=dpi)
        output_file = os.path.join(output_dir, f"page_{i+1:03d}.png")
        pix.save(output_file)
        print(f"Saved {output_file}")

    doc.close()
    print(f"Done! Images saved to: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_png.py input.pdf [output_folder] [dpi]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dpi_val = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    
    pdf_to_png(pdf_file, out_dir, dpi_val)