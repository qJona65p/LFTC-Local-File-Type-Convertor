import argparse
import sys
from pathlib import Path
from PIL import Image
import fitz

def pdf_to_images(input_path: str, output_dir: str = None, fmt: str = "png", dpi: int = 300):
    """Convert PDF pages to images (PNG, JPG, WebP, etc.)"""
    if output_dir is None:
        output_dir = str(Path(input_path))[:-4] + f"_{fmt}_pages"
    
    Path(output_dir).mkdir(exist_ok=True)
    fmt = fmt.upper()

    doc = fitz.open(input_path)
    print(f"Converting {len(doc)} page(s) from PDF to {fmt} at {dpi} DPI...")

    if ext == "JPG":
        ext = "JPEG"

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        # Convert Pixmap to PIL Image for flexible saving
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        output_file = Path(output_dir) / f"page_{i+1:04d}.{ext}"
        img.save(output_file, format=fmt, quality=95 if fmt == "JPEG" else None)
        print(f"  Saved: {output_file.name}")

    doc.close()
    print(f"Done! → {output_dir}/")

def image_to_image(input_path: str, output_dir: str = None, fmt: str = None, quality: int = 95):
    """Convert between image formats (PNG, JPG, WebP, TIFF, BMP, etc.)"""
    if not fmt:
        fmt = Path(output_dir or input_path).suffix.lower().lstrip(".")
    
    fmt = fmt.upper()
    if fmt == "JPG":
            ext = "JPEG"

    ext = fmt.lower()

    if not output_dir:
        # Auto-generate output name: image.png → image_converted.jpg
        stem = input_path       
        output_dir = f"{stem}_converted.{ext}"
    
    try:
        with Image.open(input_path) as img:
            # Handle RGBA → RGB for formats that don't support transparency (like JPG)
            if ext == "jpeg" and img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")
            
            save_kwargs = {}
            if ext == "jpeg":
                save_kwargs["quality"] = quality
            elif ext == "webp":
                save_kwargs["quality"] = quality
            
            img.save(output_dir, format=fmt, **save_kwargs)
            print(f"Converted: {input_path} → {output_dir}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local File Type Convertor - CLI edition")
    parser.add_argument("input", nargs="?", help="Input file (PDF or image)")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("-f", "--format", choices=["png", "jpg", "jpeg", "webp", "tiff", "bmp"], 
                        help="Target format (default: png for PDFs, auto from extension for images)")
    parser.add_argument("-d", "--dpi", type=int, default=300, help="DPI for PDF rendering (default: 300)")
    parser.add_argument("-q", "--quality", type=int, default=95, help="Quality for JPG/WebP (1-100)")
    parser.add_argument("--batch", action="store_true", help="Process all images in a directory")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input)

    if input_path.suffix.lower() == ".pdf":
        # PDF conversion
        pdf_to_images(str(input_path), args.output, args.format or "png", args.dpi)
    else:
        # Regular image conversion
        if args.batch and input_path.is_dir():
            for file in input_path.glob("*.*"):
                if file.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp", ".gif"]:
                    image_to_image(str(file), None, args.format, args.quality)
        else:
            image_to_image(str(input_path), args.output, args.format, args.quality)