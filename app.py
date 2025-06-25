import os
from flask import Flask, request, send_file 
from jinja2 import Template 
import pdfkit 
from datetime import datetime

app = Flask(__name__)


TEMPLATE_HTML = """

<!DOCTYPE html><html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport Quotidien des Ventes</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            margin: 40px;
            background-color: #f4f6f8;
            color: #333;
        }
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        h1 {
            font-size: 24px;
            color: #005687;
        }
        .summary {
            margin-top: 20px;
            font-size: 16px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: #fff;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #d9d9d9;
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #e8f4fa;
            color: #005687;
        }
        tfoot td {
            font-weight: bold;
            background-color: #f1f1f1;
        }
        .footer {
            margin-top: 40px;
            font-size: 13px;
            color: #777;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <h1>Rapport Quotidien - Production et Ventes</h1>
        <p>Date : {{ date }}</p>
        <p>Jour de la semaine : {{ jour_semaine }}</p>
    </header><table>
    <thead>
        <tr>
            <th>Tour</th>
            <th>Heure de sortie</th>
            <th>Heure d'arrivée</th>
            <th>Bidons Totaux</th>
            <th>Bidons Vendus</th>
            <th>Bidons avec Eau & Défauts</th>
            <th>Profit Total</th>
        </tr>
    </thead>
    <tbody>
        {% for ligne in donnees %}
        <tr>
            <td>{{ ligne.tour }}</td>
            <td>{{ ligne.heure_sortie }}</td>
            <td>{{ ligne.heure_arrivee }}</td>
            <td>{{ ligne.bidon_total }}</td>
            <td>{{ ligne.bidon_vendu }}</td>
            <td>{{ ligne.bidon_eau_defaut }}</td>
            <td>{{ ligne.profit_total }} FCFA</td>
        </tr>
        {% endfor %}
    </tbody>
    <tfoot>
        <tr>
            <td colspan="6">Total du jour</td>
            <td>{{ total_journalier }} FCFA</td>
        </tr>
    </tfoot>
</table>

<div class="summary">
    <p><strong>Résumé :</strong> {{ resume }}</p>
</div>

<div class="footer">
    Rapport généré automatiquement – {{ date }}
</div>

</body>
</html>
"""


@app.route("/generate", methods=["POST"]) 
def generate_pdf(): 
    data = request.json 
    template = Template(TEMPLATE_HTML) 
    rendered_html = template.render(**data)

    filename = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output_path = os.path.join("/tmp", filename)

    pdfkit.from_string(rendered_html, output_path)
    return send_file(output_path, as_attachment=True, download_name=filename)

# 🔽 C'est ici qu'on change :
if __name__ == "_main_": 
    port = int(os.environ.get("PORT", 5000))  # Render fournit le PORT automatiquement
    app.run(host="0.0.0.0", port=port)
