from rich.console import Console
from rich.table import Table
from rich import box

# Constantes
PMSS = 3864.00  # Plafond Mensuel de la Sécurité Sociale pour 2024
AVN_SURCPLT_SANTE = 5.00

# Taux de cotisations
TAUX_COTISATIONS = {
    # Santé
    'complementaire_sante_tr1_salarie': 1.75 / 100,
    'complementaire_sante_tr1_employeur': None,  # Si non applicable
    'complementaire_sante_tr2_salarie': 1.215 / 100,
    'complementaire_sante_tr2_employeur': None,
    'incapacite_invalidite_tr1_salarie': None,
    'incapacite_invalidite_tr1_employeur': 39.02 / PMSS / 100,  # Taux exprimé en %
    'incapacite_invalidite_tr2_salarie': 0.610 / 100,
    'incapacite_invalidite_tr2_employeur': 0.610 / 100,
    'dependance_tr1_salarie': 0.195 / 100,
    'dependance_tr1_employeur': 0.195 / 100,

    # Retraite
    'sec_soc_plaf_ret_salarie': 6.9 / 100,
    'sec_soc_plaf_ret_employeur': 8.55 / 100,
    'sec_soc_deplaf_ret_salarie': 0.4 / 100,
    'sec_soc_deplaf_ret_employeur': 2.02 / 100,
    'complementaire_tr1_salarie': 4.76 / 100,
    'complementaire_tr1_employeur': 7.14 / 100,
    'complementaire_tr2_salarie': 9.86 / 100,
    'complementaire_tr2_employeur': 14.78 / 100,

    # Autres cotisations
    'cot_famille_employeur': 3.45 / 100,
    'assurance_chomage_employeur': 4.30 / 100,
    'apec_salarie': 0.024 / 100,
    'apec_employeur': 0.036 / 100,
    'csg_deductible': 6.8 / 100,
    'csg_non_deductible': 2.9 / 100,
    'taux_impot': 8.9 / 100,
}

# Fonction pour calculer le salaire brut fiscal
def calcul_brut_fiscal(salaire_brut_base, avn_surcplt_sante, ret_conges_payes_1, ret_conges_payes_2, ind_cp_a1, cplt_10eme_cpl_a1):
    """
    Calcule le salaire brut fiscal en tenant compte des différentes primes et retenues.
    """
    return salaire_brut_base + avn_surcplt_sante - ret_conges_payes_1 - ret_conges_payes_2 + ind_cp_a1 + cplt_10eme_cpl_a1

def calcul_cotisations_sante(brut_fiscal):
    """
    Calcule les cotisations santé pour le salarié et l'employeur.
    """
    cotisations = []
    tranche2_base = max(0, brut_fiscal - PMSS)

    # Complémentaire Santé Tranche 1
    part_salarie = PMSS * TAUX_COTISATIONS['complementaire_sante_tr1_salarie']
    cotisations.append({
        'name': 'Complémentaire Santé Tranche 1',
        'taux_salarie': TAUX_COTISATIONS['complementaire_sante_tr1_salarie'],
        'taux_employeur': TAUX_COTISATIONS['complementaire_sante_tr1_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': 0.0  # Si non applicable
    })

    # Complémentaire Santé Tranche 2
    part_salarie = tranche2_base * TAUX_COTISATIONS['complementaire_sante_tr2_salarie']
    cotisations.append({
        'name': 'Complémentaire Santé Tranche 2',
        'taux_salarie': TAUX_COTISATIONS['complementaire_sante_tr2_salarie'],
        'taux_employeur': TAUX_COTISATIONS['complementaire_sante_tr2_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': 0.0
    })

    # Complémentaire Santé Surcplt
    cotisations.append({
        'name': 'Complémentaire Santé Surcplt',
        'taux_salarie': None,
        'taux_employeur': None,
        'part_salarie': AVN_SURCPLT_SANTE,  # Part fixe
        'part_employeur': 0.0
    })

    # Incapacité Invalidité Tranche 1
    part_employeur = PMSS * TAUX_COTISATIONS['incapacite_invalidite_tr1_employeur']
    cotisations.append({
        'name': 'Incapacité Invalidité Tranche 1',
        'taux_salarie': None,
        'taux_employeur': TAUX_COTISATIONS['incapacite_invalidite_tr1_employeur'],
        'part_salarie': 0.0,
        'part_employeur': part_employeur
    })

    # Incapacité Invalidité Tranche 2
    part_salarie = tranche2_base * TAUX_COTISATIONS['incapacite_invalidite_tr2_salarie']
    part_employeur = tranche2_base * TAUX_COTISATIONS['incapacite_invalidite_tr2_employeur']
    cotisations.append({
        'name': 'Incapacité Invalidité Tranche 2',
        'taux_salarie': TAUX_COTISATIONS['incapacite_invalidite_tr2_salarie'],
        'taux_employeur': TAUX_COTISATIONS['incapacite_invalidite_tr2_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    # Dépendance Tranche 1
    part_salarie = PMSS * TAUX_COTISATIONS['dependance_tr1_salarie']
    part_employeur = PMSS * TAUX_COTISATIONS['dependance_tr1_employeur']
    cotisations.append({
        'name': 'Dépendance Tranche 1',
        'taux_salarie': TAUX_COTISATIONS['dependance_tr1_salarie'],
        'taux_employeur': TAUX_COTISATIONS['dependance_tr1_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    return cotisations

def calcul_cotisations_retraite(brut_fiscal):
    """
    Calcule les cotisations retraite pour le salarié et l'employeur.
    """
    cotisations = []
    tranche2_base = max(0, brut_fiscal - PMSS)

    # Retraite Sécurité Sociale Plafonnée
    part_salarie = PMSS * TAUX_COTISATIONS['sec_soc_plaf_ret_salarie']
    part_employeur = PMSS * TAUX_COTISATIONS['sec_soc_plaf_ret_employeur']
    cotisations.append({
        'name': 'Retraite SS Plafonnée',
        'taux_salarie': TAUX_COTISATIONS['sec_soc_plaf_ret_salarie'],
        'taux_employeur': TAUX_COTISATIONS['sec_soc_plaf_ret_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    # Retraite Sécurité Sociale Déplafonnée
    part_salarie = brut_fiscal * TAUX_COTISATIONS['sec_soc_deplaf_ret_salarie']
    part_employeur = brut_fiscal * TAUX_COTISATIONS['sec_soc_deplaf_ret_employeur']
    cotisations.append({
        'name': 'Retraite SS Déplafonnée',
        'taux_salarie': TAUX_COTISATIONS['sec_soc_deplaf_ret_salarie'],
        'taux_employeur': TAUX_COTISATIONS['sec_soc_deplaf_ret_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    # Retraite Complémentaire Tranche 1
    part_salarie = PMSS * TAUX_COTISATIONS['complementaire_tr1_salarie']
    part_employeur = PMSS * TAUX_COTISATIONS['complementaire_tr1_employeur']
    cotisations.append({
        'name': 'Retraite Complémentaire Tranche 1',
        'taux_salarie': TAUX_COTISATIONS['complementaire_tr1_salarie'],
        'taux_employeur': TAUX_COTISATIONS['complementaire_tr1_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    # Retraite Complémentaire Tranche 2
    part_salarie = tranche2_base * TAUX_COTISATIONS['complementaire_tr2_salarie']
    part_employeur = tranche2_base * TAUX_COTISATIONS['complementaire_tr2_employeur']
    cotisations.append({
        'name': 'Retraite Complémentaire Tranche 2',
        'taux_salarie': TAUX_COTISATIONS['complementaire_tr2_salarie'],
        'taux_employeur': TAUX_COTISATIONS['complementaire_tr2_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    return cotisations

def calcul_autres_cotisations(brut_fiscal):
    """
    Calcule les autres cotisations comme la cotisation famille, l'assurance chômage, etc.
    """
    cotisations = []

    # Cotisation Famille
    part_employeur = brut_fiscal * TAUX_COTISATIONS['cot_famille_employeur']
    cotisations.append({
        'name': 'Cotisation Famille',
        'taux_salarie': None,
        'taux_employeur': TAUX_COTISATIONS['cot_famille_employeur'],
        'part_salarie': 0.0,
        'part_employeur': part_employeur
    })

    # Assurance Chômage
    part_employeur = brut_fiscal * TAUX_COTISATIONS['assurance_chomage_employeur']
    cotisations.append({
        'name': 'Assurance Chômage',
        'taux_salarie': None,
        'taux_employeur': TAUX_COTISATIONS['assurance_chomage_employeur'],
        'part_salarie': 0.0,
        'part_employeur': part_employeur
    })

    # Cotisation APEC
    part_salarie = brut_fiscal * TAUX_COTISATIONS['apec_salarie']
    part_employeur = brut_fiscal * TAUX_COTISATIONS['apec_employeur']
    cotisations.append({
        'name': 'Cotisation APEC',
        'taux_salarie': TAUX_COTISATIONS['apec_salarie'],
        'taux_employeur': TAUX_COTISATIONS['apec_employeur'],
        'part_salarie': part_salarie,
        'part_employeur': part_employeur
    })

    return cotisations

def calcul_csg_crds(brut_fiscal, avn_surcplt_sante):
    """
    Calcule la CSG déductible et non déductible.
    """
    base_csg_crds = brut_fiscal + avn_surcplt_sante
    csg_deductible = base_csg_crds * TAUX_COTISATIONS['csg_deductible']
    csg_non_deductible = base_csg_crds * TAUX_COTISATIONS['csg_non_deductible']

    cotisations = []

    # CSG Déductible
    cotisations.append({
        'name': 'CSG Déductible',
        'taux_salarie': TAUX_COTISATIONS['csg_deductible'],
        'taux_employeur': None,
        'part_salarie': csg_deductible,
        'part_employeur': 0.0
    })

    # CSG/CRDS Non Déductible
    cotisations.append({
        'name': 'CSG/CRDS Non Déductible',
        'taux_salarie': TAUX_COTISATIONS['csg_non_deductible'],
        'taux_employeur': None,
        'part_salarie': csg_non_deductible,
        'part_employeur': 0.0
    })

    return cotisations

def calcul_net_social(brut_fiscal, total_cotisations_salariales):
    """
    Calcule le net social avant impôt.
    """
    return brut_fiscal - total_cotisations_salariales

def calcul_net_avant_impot(net_social, tickets_restaurant_salarie, rep_avn_surcplt_ss, indemnite_telephonique):
    """
    Calcule le net avant impôt sur le revenu.
    """
    return net_social - tickets_restaurant_salarie + rep_avn_surcplt_ss + indemnite_telephonique

def calcul_prelevement_a_la_source(brut_fiscal):
    """
    Calcule le prélèvement à la source (impôt sur le revenu).
    """
    base_impot = brut_fiscal * 0.9  # Base ajustée
    return base_impot * TAUX_COTISATIONS['taux_impot']

def afficher_bulletin(console, data_bulletin):
    """
    Affiche le bulletin de paie en utilisant Rich.
    """
    console.print("[bold cyan]{:^60}[/bold cyan]\n".format("BULLETIN DE PAIE"))

    # Salaire brut fiscal
    table_brut = Table(show_header=False, box=None)
    table_brut.add_row("Salaire brut fiscal :", f"{data_bulletin['brut_fiscal']:>10.2f} €")
    console.print(table_brut)

    # Affichage des catégories de cotisations
    for category_name, cotisations in data_bulletin['cotisations'].items():
        console.print(f"\n[bold cyan]{category_name.upper():^60}[/bold cyan]")
        table = Table(
            "Libellé",
            "Taux Salarié",
            "Part Salarié",
            "Taux Employeur",
            "Part Employeur",
            title_justify="left",
            box=box.MINIMAL_DOUBLE_HEAD
        )

        for cot in cotisations:
            taux_salarie = f"{cot['taux_salarie']*100:.2f} %" if cot['taux_salarie'] is not None else "-"
            taux_employeur = f"{cot['taux_employeur']*100:.2f} %" if cot['taux_employeur'] is not None else "-"
            part_salarie = f"{cot['part_salarie']:>10.2f} €"
            part_employeur = f"{cot['part_employeur']:>10.2f} €"
            table.add_row(
                cot['name'],
                taux_salarie,
                part_salarie,
                taux_employeur,
                part_employeur
            )
        console.print(table)

    # Net social
    console.print(f"\n[bold cyan]{'NET SOCIAL':^60}[/bold cyan]")
    table_net_social = Table(show_header=False, box=None)
    table_net_social.add_row("Net social :", f"{data_bulletin['net_social']:>10.2f} €")
    console.print(table_net_social)

    # Autres éléments de paie
    console.print(f"\n[bold cyan]{'AUTRES ÉLÉMENTS DE PAIE':^60}[/bold cyan]")
    table_autres = Table(show_header=False, box=None)
    table_autres.add_row("Tickets Restaurant - Part Salarié :", f"{data_bulletin['tickets_restaurant_salarie']:>10.2f} €")
    table_autres.add_row("REP AVN Surcplt SS :", f"{data_bulletin['rep_avn_surcplt_ss']:>10.2f} €")
    table_autres.add_row("Indemnité Téléphonique :", f"{data_bulletin['indemnite_telephonique']:>10.2f} €")
    console.print(table_autres)

    # Prélèvement à la source
    console.print(f"\n[bold cyan]{'IMPÔT SUR LE REVENU':^60}[/bold cyan]")
    table_impot = Table(show_header=False, box=None)
    table_impot.add_row(f"Prélèvement à la source ({TAUX_COTISATIONS['taux_impot']*100:.2f} %) :", f"{data_bulletin['prelevement_a_la_source']:>10.2f} €")
    console.print(table_impot)

    # Net à payer
    console.print(f"\n[bold cyan]{'NET À PAYER':^60}[/bold cyan]")
    table_net_payer = Table(show_header=False, box=None)
    table_net_payer.add_row("Net à payer au salarié :", f"{data_bulletin['net_a_payer']:>10.2f} €")
    console.print(table_net_payer)

def main():
    console = Console()

    # Variables de base
    salaire_annuel_brut = 21000  # VOTRE BRUT ANNUEL ICI
    salaire_brut_base = salaire_annuel_brut / 12
    avn_surcplt_sante = AVN_SURCPLT_SANTE

    # Calcul des retenues et indemnités
    ret_conges_payes_1 = 0.5 * 204.06
    ret_conges_payes_2 = 1.0 * 204.06
    ind_cp_a1 = 1.5 * 204.06
    cplt_10eme_cpl_a1 = 1.22

    # Calcul du brut fiscal
    brut_fiscal = calcul_brut_fiscal(
        salaire_brut_base,
        avn_surcplt_sante,
        ret_conges_payes_1,
        ret_conges_payes_2,
        ind_cp_a1,
        cplt_10eme_cpl_a1
    )
    brut_fiscal = round(brut_fiscal, 2)

    # Calcul des cotisations
    cotisations_sante = calcul_cotisations_sante(brut_fiscal)
    cotisations_retraite = calcul_cotisations_retraite(brut_fiscal)
    autres_cotisations = calcul_autres_cotisations(brut_fiscal)
    cotisations_csg = calcul_csg_crds(brut_fiscal, avn_surcplt_sante)

    # Total des cotisations salariales
    total_cotisations_salariales = sum([
        cot['part_salarie'] for cot in cotisations_sante + cotisations_retraite + autres_cotisations + cotisations_csg
    ])
    total_cotisations_salariales = round(total_cotisations_salariales, 2)

    # Calcul du net social
    net_social = calcul_net_social(brut_fiscal, total_cotisations_salariales)

    # Autres éléments de paie
    tickets_restaurant_salarie = 24 * 4.00
    rep_avn_surcplt_ss = 5.00
    indemnite_telephonique = 7.50

    # Calcul du net avant impôt
    net_avant_impot = calcul_net_avant_impot(
        net_social,
        tickets_restaurant_salarie,
        rep_avn_surcplt_ss,
        indemnite_telephonique
    )

    # Calcul du prélèvement à la source
    prelevement_a_la_source = calcul_prelevement_a_la_source(brut_fiscal)
    prelevement_a_la_source = round(prelevement_a_la_source, 2)

    # Calcul du net à payer
    net_a_payer = net_avant_impot - prelevement_a_la_source
    net_a_payer = round(net_a_payer, 2)

    # Préparation des données pour l'affichage
    data_bulletin = {
        'brut_fiscal': brut_fiscal,
        'cotisations': {
            'Cotisations Santé': cotisations_sante,
            'Cotisations Retraite': cotisations_retraite,
            'Autres Cotisations': autres_cotisations,
            'CSG/CRDS': cotisations_csg
        },
        'net_social': net_social,
        'tickets_restaurant_salarie': tickets_restaurant_salarie,
        'rep_avn_surcplt_ss': rep_avn_surcplt_ss,
        'indemnite_telephonique': indemnite_telephonique,
        'prelevement_a_la_source': prelevement_a_la_source,
        'net_a_payer': net_a_payer
    }

    # Affichage du bulletin de paie
    afficher_bulletin(console, data_bulletin)

if __name__ == "__main__":
    main()
