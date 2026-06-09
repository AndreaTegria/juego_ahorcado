from flask import Flask, render_template, request, session
import random

from Paquetes import bd_palabras
from Paquetes import diagramas

app = Flask(__name__)

app.secret_key = "ahorcado123"


@app.route("/", methods=["GET", "POST"])
def inicio():

    # Crear una nueva partida
    if "palabra" not in session:

        session["palabra"] = random.choice(
            bd_palabras.bdPalabras
        ).upper()

        session["letras_adivinadas"] = []

        session["intentos"] = 7

    palabra = session["palabra"]

    letra = ""

    # Procesar letra enviada por el usuario
    if (
        request.method == "POST"
        and session["intentos"] > 0
    ):

        letra = request.form.get(
            "letra", ""
        ).upper()

        if (
            letra
            and letra.isalpha()
            and letra not in session["letras_adivinadas"]
        ):

            letras = session["letras_adivinadas"]
            letras.append(letra)
            session["letras_adivinadas"] = letras

            # Restar intento si falla
            if letra not in palabra:
                session["intentos"] -= 1

    # Construir palabra oculta
    palabra_oculta = ""

    for letra_palabra in palabra:

        if letra_palabra in session["letras_adivinadas"]:
            palabra_oculta += letra_palabra + " "
        else:
            palabra_oculta += "_"

    # Verificar victoria
    juego_ganado = True

    for letra_palabra in palabra:

        if letra_palabra not in session["letras_adivinadas"]:
            juego_ganado = False
            break

    # Verificar derrota
    juego_perdido = session["intentos"] == 0

    return render_template(
        "index.html",
        palabra_oculta=palabra_oculta,
        letras=session["letras_adivinadas"],
        intentos=session["intentos"],
        dibujo=diagramas.vidas[session["intentos"]],
        juego_ganado=juego_ganado,
        juego_perdido=juego_perdido,
        palabra=palabra
    )


@app.route("/reiniciar")
def reiniciar():

    session.clear()

    return """
    <script>
        window.location.href='/';
    </script>
    """


if __name__ == "__main__":
    app.run(debug=True)