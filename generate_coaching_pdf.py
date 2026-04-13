from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors

BLACK = colors.HexColor('#1a1a1a')
GRAY  = colors.HexColor('#555555')

s_main_title = ParagraphStyle('MainTitle', fontName='Helvetica-Bold', fontSize=14, textColor=BLACK, spaceAfter=4*mm, leading=20)
s_section     = ParagraphStyle('Section',   fontName='Helvetica-Bold', fontSize=12, textColor=BLACK, spaceAfter=3*mm, spaceBefore=6*mm, leading=18)
s_subsection  = ParagraphStyle('SubSection',fontName='Helvetica-Bold', fontSize=12, textColor=BLACK, spaceAfter=2*mm, spaceBefore=4*mm, leading=18)
s_body        = ParagraphStyle('Body',      fontName='Helvetica', fontSize=10, textColor=BLACK, spaceAfter=2*mm, leading=16)
s_body_bold   = ParagraphStyle('BodyBold',  fontName='Helvetica-Bold', fontSize=10, textColor=BLACK, spaceAfter=2*mm, leading=16)
s_small       = ParagraphStyle('Small',     fontName='Helvetica', fontSize=9,  textColor=GRAY,  spaceAfter=2*mm, leading=14)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#dddddd'), spaceAfter=3*mm, spaceBefore=1*mm)

def sp(h=3):
    return Spacer(1, h*mm)


def generate_pdf(client, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)

    story = []

    story.append(Paragraph(f"COACHING {client['nom'].upper()}", s_main_title))
    story.append(hr())

    profil_block = [
        Paragraph("Profil avant programme", s_section),
        Paragraph(f"<b>Âge – Taille – Poids – BF :</b> {client['age']} ans - {client['taille']} - {client['poids']}kg - {client['bf']}%", s_body),
        Paragraph(f"<b>Passé morpho :</b> {client['passe_morpho']}", s_body),
        Paragraph(f"<b>Objectifs :</b> {client['objectifs']}", s_body),
    ]
    if client.get('points_forts'):
        profil_block.append(Paragraph(f"<b>Points forts :</b> {client['points_forts']}", s_body))
    if client.get('points_faibles'):
        profil_block.append(Paragraph(f"<b>Points faibles :</b> {client['points_faibles']}", s_body))
    profil_block.append(hr())
    story.append(KeepTogether(profil_block))

    story.append(Paragraph("Programme d'entraînement", s_section))

    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    split_list = client['split_jours']
    split_text = "  |  ".join([f"<b>{jours[i]}</b> : {split_list[i]}" for i in range(7)])

    story.append(Paragraph("Split :", s_subsection))
    story.append(Paragraph("L'ordre des séances correspond aux jours de la semaine du lundi au dimanche.", s_small))
    story.append(sp(1))
    story.append(Paragraph(split_text, s_body))
    story.append(sp(2))

    series_block = [
        Paragraph("Séries et répétitions :", s_subsection),
        Paragraph("Échauffement : entre 1 à 2 séries en explosif avant d'arriver à la charge de travail, 1-2 min de repos", s_body),
        sp(1),
        Paragraph("Séries de travail sur les exercices polyarticulaires (bench, squat, presse, rowing, militaire) :", s_body_bold),
        Paragraph("- 1 série principale (top set) lourde de 6 à 8 répétitions, proche de l'échec ou à l'échec", s_body),
        Paragraph("- suivie de 1 série allégée (back-off set) de 8 à 12 répétitions", s_body),
        sp(1),
        Paragraph("Sur les exercices d'isolation :", s_body_bold),
        Paragraph("- 2 à 3 séries de 10 à 12 répétitions proche ou à l'échec (2 séries en upper, 2-3 en push/pull)", s_body),
        sp(1),
        Paragraph("Exception : si focus force sur un exercice (exemple : bench), 3 séries de 3 à 4 répétitions", s_small),
        sp(2),
    ]
    story.append(KeepTogether(series_block))

    seances_items = list(client['seances'].items())
    for i, (seance_name, exercices) in enumerate(seances_items):
        seance_block = []
        if i == 0:
            seance_block.append(Paragraph("Séances :", s_subsection))
            seance_block.append(sp(2))
        seance_block.append(Paragraph(f"{seance_name} :", s_subsection))
        for ex in exercices:
            seance_block.append(Paragraph(f"- {ex}", s_body))
        seance_block.append(sp(3))
        story.append(KeepTogether(seance_block))

    diete_block = []
    diete_block.append(hr())
    diete_block.append(Paragraph("Diète / Dépense", s_section))
    for semaine in client['diete_semaines']:
        diete_block.append(Paragraph(semaine, s_body))
    diete_block.append(sp(2))
    diete_block.append(Paragraph("Macros :", s_subsection))
    diete_block.append(Paragraph("- Protéines : 150g minimum", s_body))
    diete_block.append(Paragraph("- Glucides : 150g - 400g selon le total calorique", s_body))
    diete_block.append(Paragraph("- Lipides : 80g maximum", s_body))
    diete_block.append(sp(2))
    diete_block.append(Paragraph("Manger la plupart des glucides avant l'entrainement :", s_body_bold))
    diete_block.append(Paragraph("- Glucides lents (riz, pâtes, etc.) : 1-3h avant", s_body))
    diete_block.append(Paragraph("- Glucides rapides (sucre, banane, etc.) : 0-1h avant", s_body))
    diete_block.append(sp(1))
    diete_block.append(Paragraph("Manger la plupart des protéines tôt le matin ET juste après l'entraînement (minimum 40g de protéines dans chaque repas)", s_body))
    diete_block.append(hr())
    story.append(KeepTogether(diete_block))

    complements_block = [
        Paragraph("Compléments", s_section),
        Paragraph("- Créatine indispensable : 7g par jour tous les jours", s_body),
        Paragraph("- Préworkout / Boissons énergisantes : de temps en temps pour une grosse séance", s_body),
        hr(),
    ]
    story.append(KeepTogether(complements_block))

    attention_block = [
        Paragraph("Attention", s_section),
        Paragraph(
            "Le low volume (1-2 séries par exercice) surpasse en efficacité le high volume (3-4 séries) uniquement si l'intensité "
            "mise pendant ces séries est maximale. Il est indispensable de se rapprocher de l'échec musculaire (0 répétition en réserve) "
            "au maximum tout en gardant une bonne technique.", s_body),
        sp(1),
        Paragraph("L'intensité sans technique conduit inévitablement à la blessure.", s_body),
        sp(1),
        Paragraph(
            "Il convient donc d'augmenter ses charges ou son nombre de répétitions sur tous les exercices au fur et à mesure "
            "des séances en gardant une bonne technique.", s_body),
    ]
    story.append(KeepTogether(attention_block))

    doc.build(story)
