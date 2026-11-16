import sys, os, json
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = 300_000_000

src = sys.argv[1]
rows = []
for root, dirs, files in os.walk(src):
    for f in sorted(files):
        p = os.path.join(root, f)
        try:
            im = Image.open(p)
            im = ImageOps.exif_transpose(im)
            w, h = im.size
            mode = im.mode
            alpha = (mode in ("RGBA", "LA", "P") and
                     ("transparency" in im.info or mode in ("RGBA", "LA")))
            ex = im.getexif()
            gps = 34853 in ex
            rows.append(dict(name=f, rel=os.path.relpath(p, src), w=w, h=h,
                             mode=mode, alpha=bool(alpha), gps=bool(gps),
                             kb=os.path.getsize(p) // 1024,
                             ar=round(w / h, 3)))
        except Exception as e:
            rows.append(dict(name=f, rel=os.path.relpath(p, src), err=str(e)[:60]))
print(json.dumps(rows, ensure_ascii=False))
