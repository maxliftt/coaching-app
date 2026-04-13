from flask import Flask, request, jsonify, send_file
import anthropic
import json
import os
import tempfile

from generate_coaching_pdf import generate_pdf

app = Flask(__name__)

# Charge le prompt au démarrage
with open("prompt_coaching.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

client_ai = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/generate", methods=["POST"])
def generate():
    """
    Reçoit les paramètres client en JSON, appelle Claude, génère le PDF et le renvoie.

    Corps attendu (JSON) :
    {
        "nom": "Thomas",
        "age": 22,
        "taille": "1m82",
        "poids": 80,
        "bf": 12,
        "niveau": "intermédiaire",
        "jours_dispo": 5,
        "objectif": "pdm",
        "points_faibles": ["épaules", "pecs"],
        "points_forts": ["dos", "jambes"],
        "objectif_force": null,
        "passe_morpho": "mince, peu de masse musculaire"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Corps JSON manquant"}), 400

        # Vérifie les champs obligatoires
        required = ["nom", "age", "taille", "poids", "bf", "niveau",
                    "jours_dispo", "objectif", "passe_morpho"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Champ manquant : {field}"}), 400

        # Formate le message client pour Claude
        user_message = f"""
Génère le programme pour ce client :
- nom: {data['nom']}
- age: {data['age']}
- taille: {data['taille']}
- poids: {data['poids']}kg
- bf: {data['bf']}%
- niveau: {data['niveau']}
- jours_dispo: {data['jours_dispo']}
- objectif: {data['objectif']}
- points_faibles: {', '.join(data.get('points_faibles', [])) or 'aucun'}
- points_forts: {', '.join(data.get('points_forts', [])) or 'aucun'}
- objectif_force: {data.get('objectif_force') or 'null'}
- passe_morpho: {data['passe_morpho']}
"""

        # Appel à Claude
        response = client_ai.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        raw = response.content[0].text.strip()

        # Parse le JSON retourné par Claude
        try:
            client_data = json.loads(raw)
        except json.JSONDecodeError:
            # Tentative de nettoyage si Claude a mis des backticks
            clean = raw.replace("```json", "").replace("```", "").strip()
            client_data = json.loads(clean)

        # Génère le PDF dans un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            pdf_path = tmp.name

        generate_pdf(client_data, pdf_path)

        filename = f"Coaching_{client_data['nom']}.pdf"
        return send_file(
            pdf_path,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
