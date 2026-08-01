"""
============================================================
RECORTE AUTOMÁTICO DE FOTOS - Marie Kids Catálogo
============================================================
Recorta todas las fotos de producto a la proporción 15:16
(la misma proporción del cuadro .photo3 en el catálogo),
centrando el producto, para que llenen el marco sin dejar
espacios crema ni cortar partes importantes.

CÓMO USARLO:
1. Instala Pillow (una sola vez):
       pip install pillow

2. Abre este archivo y edita las 2 líneas marcadas como
   CARPETA_ORIGEN y CARPETA_DESTINO más abajo.

3. Ejecuta:
       python recortar_fotos_15_16.py

4. Revisa la carpeta de destino: tendrá la MISMA estructura
   de subcarpetas que tu carpeta "img/" original, pero con
   las fotos ya recortadas. Tus fotos originales NO se tocan
   ni se sobrescriben.

5. Si te gusta el resultado, reemplaza tu carpeta img/ por la
   nueva (o copia los archivos encima), y listo.
============================================================
"""

from pathlib import Path
from PIL import Image, ImageOps

# ------------------------------------------------------------------
# 1) EDITA ESTAS DOS RUTAS ANTES DE EJECUTAR
# ------------------------------------------------------------------
CARPETA_ORIGEN = Path("img")              # tu carpeta actual de fotos
CARPETA_DESTINO = Path("img_recortadas")  # carpeta nueva (se crea sola)

# ------------------------------------------------------------------
# 2) Proporción objetivo: 15:16 (ancho:alto) = la de .photo3
#    Puedes ajustar el tamaño de salida si quieres más resolución.
# ------------------------------------------------------------------
ANCHO_SALIDA = 1000
ALTO_SALIDA = 1065  # 1000 * (16/15) ≈ 1065

EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".webp"}


def recortar_centrado(imagen: Image.Image, ancho_obj: int, alto_obj: int) -> Image.Image:
    """
    Recorta la imagen al centro para que coincida con la proporción
    ancho_obj:alto_obj, sin deformarla, y luego la redimensiona al
    tamaño de salida exacto.
    """
    # Corrige la orientación según metadatos EXIF (fotos de celular)
    imagen = ImageOps.exif_transpose(imagen)
    imagen = imagen.convert("RGB")

    ancho_img, alto_img = imagen.size
    ratio_obj = ancho_obj / alto_obj
    ratio_img = ancho_img / alto_img

    if ratio_img > ratio_obj:
        # La imagen es más ANCHA de lo necesario -> recortar los lados
        nuevo_ancho = int(alto_img * ratio_obj)
        margen = (ancho_img - nuevo_ancho) // 2
        caja = (margen, 0, margen + nuevo_ancho, alto_img)
    else:
        # La imagen es más ALTA de lo necesario -> recortar arriba/abajo
        nuevo_alto = int(ancho_img / ratio_obj)
        margen = (alto_img - nuevo_alto) // 2
        caja = (0, margen, ancho_img, margen + nuevo_alto)

    recortada = imagen.crop(caja)
    return recortada.resize((ancho_obj, alto_obj), Image.LANCZOS)


def procesar_carpeta(origen: Path, destino: Path):
    if not origen.exists():
        print(f"❌ No encuentro la carpeta '{origen}'. Revisa la ruta CARPETA_ORIGEN.")
        return

    archivos = [
        p for p in origen.rglob("*")
        if p.is_file() and p.suffix.lower() in EXTENSIONES_VALIDAS
    ]

    if not archivos:
        print(f"⚠️  No se encontraron imágenes en '{origen}'.")
        return

    print(f"Encontradas {len(archivos)} imágenes. Procesando...\n")

    ok, fallidas = 0, []
    for ruta in archivos:
        ruta_relativa = ruta.relative_to(origen)
        ruta_salida = destino / ruta_relativa
        ruta_salida.parent.mkdir(parents=True, exist_ok=True)

        try:
            with Image.open(ruta) as img:
                resultado = recortar_centrado(img, ANCHO_SALIDA, ALTO_SALIDA)
                # PNG se guarda como PNG (por transparencia), el resto como JPG
                if ruta.suffix.lower() == ".png":
                    resultado.save(ruta_salida, optimize=True)
                else:
                    resultado.save(ruta_salida.with_suffix(".jpg"), "JPEG", quality=88, optimize=True)
            ok += 1
            print(f"  ✅ {ruta_relativa}")
        except Exception as e:
            fallidas.append((ruta_relativa, str(e)))
            print(f"  ❌ {ruta_relativa}  ->  {e}")

    print(f"\n============================================================")
    print(f"Listo: {ok} imágenes recortadas correctamente.")
    if fallidas:
        print(f"{len(fallidas)} fallaron:")
        for nombre, error in fallidas:
            print(f"   - {nombre}: {error}")
    print(f"Resultado guardado en: {destino.resolve()}")
    print(f"============================================================")


if __name__ == "__main__":
    procesar_carpeta(CARPETA_ORIGEN, CARPETA_DESTINO)
