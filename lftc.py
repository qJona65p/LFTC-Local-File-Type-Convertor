import argparse
import sys
from pathlib import Path
from PIL import Image
import fitz

def pdf_to_images(input_path: str, output_dir: str = None, fmt: str = "png", dpi: int = 300):
    """Convert PDF pages to images"""
    if output_dir is None:
        output_dir = Path(input_path).stem + f"_{fmt}_pages"
    
    Path(output_dir).mkdir(exist_ok=True)
    fmt = fmt.upper()

    doc = fitz.open(input_path)
    print(f"Converting {len(doc)} page(s) from PDF to {fmt} at {dpi} DPI...")

    if fmt == "JPG":
        fmt = "JPEG"

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        # Convert Pixmap to PIL Image for flexible saving
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        output_file = Path(output_dir) / f"page_{i+1:04d}.{fmt.lower()}"
        img.save(output_file, format=fmt, quality=95 if fmt == "JPEG" else None)
        print(f"  Saved: {output_file.name}")

    doc.close()
    print(f"Done! → {output_dir}/")

def image_to_image(input_path: str, output_dir: str = None, fmt: str = None, quality: int = 95):
    """Convert between image formats (PNG, JPG, WebP, TIFF, BMP, etc.)"""
    if not fmt:
        print("No format was given for image conversion.")
        sys.exit(1)
    
    fmt = fmt.upper()
    if fmt == "JPG":
        fmt = "JPEG"

    if not output_dir:
        # Auto-generate output name: image.png → image_converted.jpg
        stem = Path(input_path).stem
        output_dir = f"{stem}_converted.{fmt.lower()}"
    
    try:
        with Image.open(input_path) as img:
            # Handle RGBA → RGB for formats that don't support transparency
            if fmt == "JPEG" and img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")
            
            save_kwargs = {}
            if fmt == "JPEG":
                save_kwargs["quality"] = quality
            elif fmt == "WEBP":
                save_kwargs["quality"] = quality
            
            img.save(output_dir, format=fmt, **save_kwargs)
            print(f"Converted: {input_path} → {output_dir}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def audio_to_audio():
    print("Audio is WIP")
    pass

def main():
    audio_fmts = ["mp3", "wav", "ogg", "flac", "m4a", "aac", "opus", "wma"]
    image_fmts = ["png", "jpg", "jpeg", "webp", "tiff", "bmp"]
    parser = argparse.ArgumentParser(description="Local File Type Convertor - CLI edition")
    parser.add_argument("input", nargs="?", help="Input file (PDF, image or dir)")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument("-f", "--format", 
                        choices=audio_fmts+image_fmts,
                        help="Target format")
    parser.add_argument("-d", "--dpi", type=int, default=300, help="DPI for PDF rendering (default: 300)")
    parser.add_argument("-q", "--quality", type=int, default=95, help="Quality for JPG/WebP (1-100)")
    parser.add_argument("-b", "--bitrate", default="192k", help="Bitrate for audio (e.g. 128k, 320k)")
    parser.add_argument("--batch", action="store_true", help="Process all images in a directory")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input)

    if input_path.suffix.lower() == ".pdf":
        # PDF conversion
        pdf_to_images(str(input_path), args.output, args.format or "png", args.dpi)
        return
    
    # Image handling
    if args.format in image_fmts or input_path.suffix.lower() in image_fmts:
        if args.batch and input_path.is_dir():
            # Batch conversion
            for file in input_path.glob("*.*"):
                if file.suffix.lower()[1:] in image_fmts:
                    image_to_image(str(file), None, args.format, args.quality)
        else:
            # Single conversion
            image_to_image(str(input_path), args.output, args.format, args.quality)
        return

    # Audio handling
    if args.format in audio_fmts or input_path.suffix.lower() in audio_fmts:
        if args.batch and input_path.is_dir():
            # Batch conversion
            for file in input_path.glob("*.*"):
                if file.suffix.lower()[1:] in audio_fmts:
                    audio_to_audio()
        else:
            # Single conversion
            audio_to_audio()
        return

if __name__ == "__main__":
    main()