import streamlit as st
import math
import matplotlib.pyplot as plt
import urllib.parse

# =============================
# CONFIG GENERAL
# =============================
st.set_page_config(
    page_title="Madera Precisa",
    page_icon="🪵",
    layout="wide"
)

# =============================
# CSS
# =============================
st.markdown("""
<style>
.card {
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 18px;
    background-color: #ffffff;
    margin-bottom: 16px;
}
.precio {
    font-size: 36px;
    font-weight: 800;
}
.sub {
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# =============================
# DATOS
# =============================
PRECIO_M2 = 350
FACTOR_UTILIDAD = 2.2
DESPERDICIO = 0.15
COSTO_CAJON = 800
COSTO_PUERTAS = 3500
ANCHO_MODULO = 600

COLORES_MDF = {
    "Blanco": "#F5F5F5",
    "Nogal": "#7A4A2E",
    "Roble": "#C19A6B",
    "Gris": "#B0B0B0"
}

PRECIOS_TABLAS = {
    "Pino": [
        (1, 9, 145, 95, "Precio menudeo"),
        (10, 24, 125, 75, "Buen margen para empezar"),
        (25, 49, 110, 60, "Precio de distribuidor"),
        (50, 99, 95, 45, "Precio preferente"),
        (100, 9999, 85, 35, "Precio volumen"),
    ],
    "Cedro": [
        (1, 9, 345, 225, "Precio menudeo"),
        (10, 24, 300, 180, "Buen margen para empezar"),
        (25, 49, 265, 145, "Precio de distribuidor"),
        (50, 99, 225, 105, "Precio preferente"),
        (100, 9999, 205, 85, "Precio volumen"),
    ]
}


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.image("logo_madera_precisa.png", width=310)
    opcion = st.radio(
        "Servicio",
        ["Closets", "Tablas de picar"]
    )


# ======================================================
# ======================= CLOSETS =======================
# ======================================================
if opcion == "Closets":

    st.title("Closet a medida")

    # =============================
    # INPUTS (sin render todavía)
    # =============================
    col1, col2 = st.columns(2)

    with col1:
        alto = st.slider("Alto (mm)", 2000, 3000, 2400, 50)
        ancho = st.slider("Ancho (mm)", 1200, 6000, 2400, 50)
        maletero_altura = st.slider("Altura maletero (mm)", 300, 600, 400, 10)

    with col2:
        color = st.selectbox("Color MDF", COLORES_MDF.keys())
        cajones = st.number_input("Cajones", 0, 12, 4)
        puertas = st.checkbox("Agregar puertas")

    # =============================
    # CÁLCULOS
    # =============================
    modulos = math.ceil(ancho / ANCHO_MODULO)

    area_total = (
        (modulos + 1) * (alto * 600) +
        modulos * 3 * (600 * 600) +
        ancho * maletero_altura
    ) / 1_000_000

    area_total *= (1 + DESPERDICIO)

    costo = area_total * PRECIO_M2
    precio_final = costo * FACTOR_UTILIDAD
    precio_final += cajones * COSTO_CAJON
    precio_final += COSTO_PUERTAS if puertas else 0

    # =============================
    # PRECIO + RENDER (ARRIBA)
    # =============================
    col_price, col_render = st.columns([1, 2])

    with col_price:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='precio'>${precio_final:,.0f} MXN</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sub'>{modulos} módulos · {cajones} cajones · {color}</div>", unsafe_allow_html=True)
        st.markdown("Incluye maletero superior")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_render:
        fig, ax = plt.subplots(figsize=(11, 4))

        alto_total = 3
        alto_maletero = max(0.6, alto_total * (maletero_altura / alto))
        alto_cuerpo = alto_total - alto_maletero

        cajones_restantes = cajones

        for i in range(modulos):
            ax.add_patch(plt.Rectangle((i, 0), 1, alto_cuerpo,
                facecolor=COLORES_MDF[color], edgecolor="black"))

            ax.add_patch(plt.Rectangle((i, alto_cuerpo), 1, alto_maletero,
                facecolor="#BDBDBD", edgecolor="black", linewidth=2))

            if cajones_restantes > 0:
                for j in range(min(3, cajones_restantes)):
                    ax.add_patch(plt.Rectangle(
                        (i + 0.15, j * 0.35 + 0.1),
                        0.7, 0.25,
                        facecolor="#E6D3B1",
                        edgecolor="black"
                    ))
                cajones_restantes -= 3

        ax.set_xlim(0, modulos)
        ax.set_ylim(0, alto_total)
        ax.axis("off")
        st.pyplot(fig)

    # =============================
    # WHATSAPP
    # =============================
    msg = f"Closet a medida\n{modulos} módulos\nPrecio: ${precio_final:,.0f} MXN"
    st.markdown(f"[📲 Enviar por WhatsApp](https://wa.me/?text={urllib.parse.quote(msg)})")

# ======================================================
# =================== TABLAS PICAR =====================
# ======================================================
elif opcion == "Tablas de picar":

    st.title("Tablas de picar – Precios por volumen")

    col1, col2 = st.columns(2)

    # =============================
    # COLUMNA 1: MADERA + IMAGEN
    # =============================
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        madera = st.selectbox("Madera", PRECIOS_TABLAS.keys())

        # Imagen según madera
        if madera == "Pino":
            st.image("pino.png", width="stretch")
        elif madera == "Cedro":
            st.image("cedro.png", width="stretch")

        st.markdown("</div>", unsafe_allow_html=True)

    # =============================
    # COLUMNA 2: CANTIDAD + PRECIO
    # =============================
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        cantidad = st.number_input("Cantidad", 1, 500, 10)

        precio_unit = utilidad = msg = 0

        for a, b, p, u, t in PRECIOS_TABLAS[madera]:
            if a <= cantidad <= b:
                precio_unit = p
                utilidad = u
                msg = t
                break

        total = precio_unit * cantidad
        margen = utilidad / precio_unit * 100 if precio_unit else 0

        st.markdown(
            f"<div class='precio'>${total:,.0f} MXN</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='sub'>{cantidad} piezas · ${precio_unit} c/u · Margen {margen:.0f}%</div>",
            unsafe_allow_html=True
        )

        st.success(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    # =============================
    # TABLA DE REFERENCIA
    # =============================
    st.subheader("📊 Precios de referencia por volumen")

    tabla_ref = []
    for a, b, p, u, t in PRECIOS_TABLAS[madera]:
        rango = f"{a}–{b if b < 9999 else '+'}"
        tabla_ref.append({
            "Cantidad": rango,
            "Precio unitario ($)": p,
            "Utilidad ($)": u,
            "Mensaje": t
        })

    st.dataframe(
        tabla_ref,
        width="stretch"
    )
