import os
from flask import Flask, request, send_file, jsonify
import pdfkit
from datetime import datetime

app = Flask(__name__)

def generate_html(data):
    """
    Construit le HTML du rapport à partir du dictionnaire `data`.
    """
    # Récupération des champs avec valeurs par défaut si absent
    date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    jour = data.get("jour_semaine", datetime.now().strftime("%A"))
    lignes = data.get("donnees", [])
    total = data.get("total_journalier", sum(l.get("profit_total", 0) for l in lignes))
    resume = data.get("resume", "")
    stock_bouchons = data.get("total_bouchons", "N/A")
    stock_etiquettes = data.get("total_etiquettes", "N/A")
    stock_trompettes = data.get("total_trompettes", "N/A")

    # Construction du HTML
    html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Rapport journalier - {date}</title>
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #ffffff;
      color: #000;
    }}
    .header {{
      background-color: #3c4c44;
      color: white;
      padding: 40px 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .logo {{
      font-size: 24px;
      font-weight: bold;
      border: 2px solid white;
      padding: 10px 20px;
      border-radius: 50%;
      text-align: center;
    }}
    .company-info {{
      text-align: right;
      font-size: 14px;
    }}
    .reference {{
      padding: 30px;
      font-size: 14px;
      display: flex;
      justify-content: space-between;
    }}
    .table-container {{
      padding: 0 30px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }}
    th, td {{
      padding: 12px;
      border-bottom: 1px solid #ccc;
      text-align: center;
    }}
    th {{
      border-top: 1px solid #ccc;
    }}
    .stocks {{
      padding: 0 30px;
      font-size: 14px;
      margin-top: 20px;
      line-height: 1.6em;
    }}
    .total {{
      padding: 30px;
      text-align: right;
      font-weight: bold;
      font-size: 18px;
    }}
  </style>
</head>
<body>

  <div class="header">
    <div class="logo">DBD<br>SARL</div>
    <div class="company-info">
      <div>Rapport Journalier - Usine</div>
      <div>37, Rue Mombele, C/ Limete</div>
    </div>
  </div>

  <div class="reference">
    <div>
      <div>En référence</div>
      <div>+243828474696</div>
      <div>37, Rue Mombele, C/ Limete</div>
      <div>{jour}</div>
    </div>
    <div>{date}</div>
  </div>

  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Tour</th>
          <th>Heure Sortie</th>
          <th>Heure Arrivée</th>
          <th>Nbre de Bidons</th>
          <th>Vendu</th>
          <th>Eau & Défauts</th>
          <th>Profit Total</th>
        </tr>
      </thead>
      <tbody>
        {''.join(f'''
          <tr>
            <td>{ligne.get("tour", "")}</td>
            <td>{ligne.get("heure_sortie", "")}</td>
            <td>{ligne.get("heure_arrivee", "")}</td>
            <td>{ligne.get("bidon_total", "")}</td>
            <td>{ligne.get("bidon_vendu", "")}</td>
            <td>{ligne.get("bidon_eau_defaut", "")}</td>
            <td>{ligne.get("profit_total", "")} FC</td>
          </tr>''' for ligne in lignes)}
      </tbody>
    </table>
  </div>

  <div class="stocks">
    <p>📦 <strong>Stock Bouchons :</strong> {stock_bouchons}</p>
    <p>🏷️ <strong>Stock Étiquettes :</strong> {stock_etiquettes}</p>
    <p>🎺 <strong>Stock Trompettes :</strong> {stock_trompettes}</p>
  </div>

  <div class="total">Total du jour : {total} FC</div>

</body>
</html>
"""
    return html

@app.route("/generate", methods=["POST"])
def generate_pdf():
    """
    Endpoint POST /generate
    Attends un JSON dans request.json,
    génère le PDF et le renvoie en attachment.
    """
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Aucun JSON fourni"}), 400

    # Générer le HTML depuis la fonction
    html_content = generate_html(data)

    # Nom et chemin du fichier de sortie
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rapport_{timestamp}.pdf"
    output_path = os.path.join("/tmp", filename)

    # Générer le PDF
    try:
        pdfkit.from_string(html_content, output_path)
    except Exception as e:
        return jsonify({"error": "Échec génération PDF", "details": str(e)}), 500

    # Renvoyer le PDF
    return send_file(output_path, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Désactive le mode debug en production
    app.run(host="0.0.0.0", port=port, debug=False)
