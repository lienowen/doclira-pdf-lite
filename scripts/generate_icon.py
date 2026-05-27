from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "doclira_lite.ico"


def font(size):
    path = Path(r"C:\Windows\Fonts\segoeuib.ttf")
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (256, 256), (6, 124, 112, 255))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((16, 16, 240, 240), radius=44, fill=(6, 124, 112, 255))
    text = "D"
    text_font = font(152)
    box = draw.textbbox((0, 0), text, font=text_font)
    x = (256 - (box[2] - box[0])) / 2
    y = (256 - (box[3] - box[1])) / 2 - 10
    draw.text((x, y), text, font=text_font, fill="white")
    image.save(OUT, sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])
    print(OUT)


if __name__ == "__main__":
    main()
