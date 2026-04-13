from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import sys

# ─── FONTS ───────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('Poppins', 'Poppins-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Poppins-Bold', 'Poppins-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DMSerif', 'DejaVuSerif-Bold.ttf'))

# ─── STYLES ──────────────────────────────────────────────────────────────────
BLACK = colors.HexColor('#1a1a1a')
GRAY  = colors.HexColor('#555555')

s_main_title = ParagraphStyle('MainTitle', fontName='DMSerif', fontSize=22, textColor=BLACK, spaceAfter=4*mm, leading=30)
s_section     = ParagraphStyle('Section',   fontName='DMSerif', fontSize=13, textColor=BLACK, spaceAfter=3*mm, spaceBefore=6*mm, leading=20)
s_subsection  = ParagraphStyle('SubSection',fontName='Poppins-Bold', fontSize=10, textColor=BLACK, spaceAfter=2*mm, spaceBefore=4*mm)
s_body        = ParagraphStyle('Body',      fontName='Poppins', fontSize=10, textColor=BLACK, spaceAfter=2*mm, leading=16)
s_body_bold   = ParagraphStyle('BodyBold',  fontName='Poppins-Bold', fontSize=10, textColor=BLACK, spaceAfter=2*mm, leading=16)
s_small       = ParagraphStyle('Small',     fontName='Poppins', fontSize=9,  textColor=GRAY,  spaceAfter=2*mm, leading=14)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#dddddd'), spaceAfter=3*mm, spaceBefore=1*mm)

def sp(h=3):
    return Spacer(1, h*mm)


def generate_pdf(client, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    story = []

    # ── TITRE ─────────────────────────────────────────────────────────────────
    story.append(Paragraph(f"COACHING {client['nom'].upper()}", s_main_title))
    story.append(hr())

    # ── PROFIL ────────────────────────────────────────────────────────────────
    story.append(Paragraph("Profil avant programme", s_section))
    story.append(Paragraph(
        f"<b>Âge – Taille – Poids – BF :</b> {client['age']} ans – {client['taille']} – {client['poids']}kg – {client['bf']}%",
        s_body))
    story.append(Paragraph(f"<b>Passé morpho :</b> {client['passe_morpho']}", s_body))
    story.append(Paragraph(f"<b>Objectifs :</b> {client['objectifs']}", s_body))
    if client.get('points_forts'):
        story.append(Paragraph(f"<b>Points forts :</b> {client['points_forts']}", s_body))
    if client.get('points_faibles'):
        story.append(Paragraph(f"<b>Points faibles :</b> {client['points_faibles']}", s_body))
    story.append(hr())

    # ── PROGRAMME ENTRAÎNEMENT ────────────────────────────────────────────────
    story.append(Paragraph("Programme d'entraînement", s_section))

    # Build split display jour par jour
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    split_list = client['split_jours']  # liste de 7 éléments, ex: ["Upper","Lower","Repos","Upper","Lower","Repos","Repos"]
    split_text = "  |  ".join([f"<b>{jours[i]}</b> : {split_list[i]}" for i in range(7)])

    story.append(Paragraph("Split :", s_subsection))
    story.append(Paragraph("L'ordre des séances correspond aux jours de la semaine du lundi au dimanche.", s_small))
    story.append(sp(1))
    story.append(Paragraph(split_text, s_body))
    story.append(sp(2))

    story.append(Paragraph("Séries et répétitions :", s_subsection))
    story.append(Paragraph(
        "Échauffement : entre 1 à 2 séries en explosif (rapide) avant d'arriver à la charge de travail, 1-2 min de repos",
        s_body))
    story.append(sp(1))
    story.append(Paragraph("Séries de travail sur les exercices polyarticulaires (bench, squat, presse, rowing, militaire) :", s_body_bold))
    story.append(Paragraph("– 1 série principale (top set) lourde de 6 à 8 répétitions, proche de l'échec ou à l'échec", s_body))
    story.append(Paragraph("– suivie de 1 série allégée (back-off set) de 8 à 12 répétitions", s_body))
    story.append(sp(1))
    story.append(Paragraph("Sur les exercices d'isolation :", s_body_bold))
    story.append(Paragraph("– 2 à 3 séries de 10 à 12 répétitions proche ou à l'échec (2 séries en upper, 2-3 en push/pull)", s_body))
    story.append(sp(1))
    story.append(Paragraph("Exception : si focus force sur un exercice (exemple : bench), 3 séries de 3 à 4 répétitions", s_small))
    story.append(sp(2))

    story.append(Paragraph("Séances :", s_subsection))
    story.append(sp(4))
    for seance_name, exercices in client['seances'].items():
        seance_block = [Paragraph(f"{seance_name} :", s_body_bold)]
        for ex in exercices:
            seance_block.append(Paragraph(f"– {ex}", s_body))
        seance_block.append(sp(3))
        story.append(KeepTogether(seance_block))

    # ── DIÈTE — tout sur la même page ─────────────────────────────────────────
    diete_block = []
    diete_block.append(hr())
    diete_block.append(Paragraph("Diète / Dépense", s_section))
    for semaine in client['diete_semaines']:
        diete_block.append(Paragraph(semaine, s_body))
    diete_block.append(sp(2))
    diete_block.append(Paragraph("Macros :", s_subsection))
    diete_block.append(Paragraph("– Protéines : 150g minimum", s_body))
    diete_block.append(Paragraph("– Glucides : 150g – 400g selon le total calorique", s_body))
    diete_block.append(Paragraph("– Lipides : 80g maximum", s_body))
    diete_block.append(sp(2))
    diete_block.append(Paragraph("Manger la plupart des glucides avant l'entraînement :", s_body_bold))
    diete_block.append(Paragraph("– Glucides lents (riz, pâtes, etc.) : 1-3h avant", s_body))
    diete_block.append(Paragraph("– Glucides rapides (sucre, banane, etc.) : 0-1h avant", s_body))
    diete_block.append(sp(1))
    diete_block.append(Paragraph("Manger la plupart des protéines tôt le matin ET juste après l'entraînement (minimum 40g de protéines dans chaque repas)", s_body))
    diete_block.append(hr())
    story.append(KeepTogether(diete_block))

    # ── COMPLÉMENTS ───────────────────────────────────────────────────────────
    story.append(Paragraph("Compléments", s_section))
    story.append(Paragraph("– Créatine indispensable : 7g par jour tous les jours", s_body))
    story.append(Paragraph("– Préworkout / Boissons énergisantes : de temps en temps pour une grosse séance", s_body))
    story.append(hr())

    # ── ATTENTION ─────────────────────────────────────────────────────────────
    story.append(Paragraph("Attention", s_section))
    story.append(Paragraph(
        "Le low volume (1-2 séries par exercice) surpasse en efficacité le high volume (3-4 séries) uniquement si l'intensité "
        "mise pendant ces séries est maximale. Il est indispensable de se rapprocher de l'échec musculaire (0 répétition en réserve) "
        "au maximum tout en gardant une bonne technique.",
        s_body))
    story.append(sp(1))
    story.append(Paragraph("L'intensité sans technique conduit inévitablement à la blessure.", s_body))
    story.append(sp(1))
    story.append(Paragraph(
        "Il convient donc d'augmenter ses charges ou son nombre de répétitions sur tous les exercices au fur et à mesure "
        "des séances en gardant une bonne technique.",
        s_body))

    doc.build(story)
    print(f"PDF généré : {output_path}")


# ─── EXEMPLE CLIENT TEST ──────────────────────────────────────────────────────
client_test = {
    "nom": "Louis",
    "age": 23,
    "taille": "1m76",
    "poids": 81,
    "bf": 30,
    "passe_morpho": "skinnyfat",
    "objectifs": "– gras (grosse priorité), + tracé",
    "points_forts": "jambes, bras",
    "points_faibles": "arrière d'épaules",
    # objectif: "seche" ou "pdm" — détermine si cardio/carbs sont affichés
    "objectif": "seche",
    "split_jours": ["Push", "Pull", "Legs", "Carbs", "Upper", "Cardio", "Repos"],
    "seances": {
        "Push": [
            "Pecfly 2",
            "Fly unilatéral poulie à hauteur moyenne 2",
            "Développé militaire 2",
            "Élévations latérales 2",
            "Barre au front 2",
            "Extensions overhead 2",
        ],
        "Pull": [
            "Facepull 3",
            "Tirage vertical 2",
            "Rowing barre 2",
            "Tirage diagonal unilatéral poulie haute sur banc incliné 2",
            "Curl biceps 2",
            "Curl marteau 2",
        ],
        "Legs": [
            "Presse 2",
            "Leg extension 3",
            "Leg curl 2",
            "Adducteurs 2",
            "Mollets 3",
        ],
        "Carbs (Cardio + Abdos)": [
            "Relevé de jambes suspendu à la barre ou chaise romaine 2",
            "Crunch poulie 3",
            "Crunch oblique 2",
            "30 min cardio au choix",
        ],
        "Upper": [
            "Facepull 3",
            "Pecfly 2",
            "Développé militaire 2",
            "Tirage vertical 2",
            "Élévations latérales 2",
            "Curl biceps 2",
            "Extensions triceps overhead 2",
        ],
    },
    "diete_semaines": [
        "Semaine 1 : 2500 kcals – 10k steps",
        "Semaine 2 : 2200 kcals – 12k steps",
        "Semaine 3 : 1900 kcals – 15k steps",
        "Semaine 4 : 1800 kcals – 17k steps",
    ],
}

generate_pdf(client_test, "/mnt/user-data/outputs/Coaching_Test.pdf")
