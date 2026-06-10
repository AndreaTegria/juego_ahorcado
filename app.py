from flask import Flask, render_template, request, session, jsonify
import random
 
from Paquetes import bd_palabras
from Paquetes import diagramas
 
app = Flask(__name__)
app.secret_key = "ahorcado123"
 
 
@app.route("/", methods=["GET"])
def inicio():
    if "palabra" not in session:
        entrada = random.choice(bd_palabras.bdPalabras)
        session["palabra"] = entrada["word"]
        session["pista"] = entrada["hint"]
        session["traduccion"] = entrada["translation"]
        session["ejemplo"] = entrada["example"]
        session["ejemplo_traduccion"] = entrada["example_translation"]
        session["letras_adivinadas"] = []
        session["intentos"] = 7
 
    return render_template(
        "index.html",
        pista=session.get("pista", ""),
        traduccion=session.get("traduccion", ""),
        ejemplo=session.get("ejemplo", ""),
        ejemplo_traduccion=session.get("ejemplo_traduccion", ""),
        palabra_oculta=obtener_palabra_oculta(),
        letras=session["letras_adivinadas"],
        intentos=session["intentos"],
        dibujo=diagramas.vidas[session["intentos"]],
        juego_ganado=verificar_ganado(),
        juego_perdido=session["intentos"] == 0,
        palabra=session["palabra"]
    )
 
 
@app.route("/letra", methods=["POST"])
def procesar_letra():
    data = request.get_json()
    letra = data.get("letra", "").upper()
 
    palabra = session.get("palabra", "")
    juego_ganado = verificar_ganado()
    juego_perdido = session["intentos"] == 0
 
    if not juego_ganado and not juego_perdido:
        if (
            letra
            and letra.isalpha()
            and letra not in session["letras_adivinadas"]
        ):
            letras = session["letras_adivinadas"]
            letras.append(letra)
            session["letras_adivinadas"] = letras
 
            if letra not in palabra:
                session["intentos"] -= 1
 
    juego_ganado = verificar_ganado()
    juego_perdido = session["intentos"] == 0
 
    return jsonify({
        "palabra_oculta": obtener_palabra_oculta(),
        "letras": session["letras_adivinadas"],
        "intentos": session["intentos"],
        "dibujo": diagramas.vidas[session["intentos"]],
        "juego_ganado": juego_ganado,
        "juego_perdido": juego_perdido,
        "palabra": palabra,
        "pista": session.get("pista", ""),
        "traduccion": session.get("traduccion", ""),
        "ejemplo": session.get("ejemplo", ""),
        "ejemplo_traduccion": session.get("ejemplo_traduccion", "")
    })
 
 
@app.route("/reiniciar")
def reiniciar():
    session.clear()
    return """
    <script>
        window.location.href='/';
    </script>
    """
 
 
def obtener_palabra_oculta():
    palabra = session.get("palabra", "")
    letras_adivinadas = session.get("letras_adivinadas", [])
    resultado = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            resultado += letra + " "
        else:
            resultado += "_ "
    return resultado.strip()
 
 
def verificar_ganado():
    palabra = session.get("palabra", "")
    letras_adivinadas = session.get("letras_adivinadas", [])
    for letra in palabra:
        if letra not in letras_adivinadas:
            return False
    return True
 
 
if __name__ == "__main__":
    app.run(debug=True)