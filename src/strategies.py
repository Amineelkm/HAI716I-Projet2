"""Les 5 stratégies du cours 4 (diapo 64) : strategie(mon_hist, hist_adv, rng) -> 'C' ou 'D'."""

def all_d(mon_hist, hist_adv, rng):
    """ALL-D : trahit à chaque tour."""
    return 'D'


def random_strat(mon_hist, hist_adv, rng):
    """RANDOM : C ou D avec une probabilité de 50 % chacun."""
    return 'C' if rng.random() < 0.5 else 'D'


def tit_for_tat(mon_hist, hist_adv, rng):
    """TIT-FOR-TAT : coopère au premier tour, puis copie le dernier coup adverse."""
    if not hist_adv:
        return 'C'
    return hist_adv[-1]


def tester(mon_hist, hist_adv, rng):
    """TESTER : D au tour 1, C au tour 2 ; si l'adversaire riposte (D au tour 2) -> TFT,
    sinon cycle C, C, D."""
    tour = len(mon_hist)          # 0 = premier tour
    if tour == 0:
        return 'D'
    if tour == 1:
        return 'C'
    if hist_adv[1] == 'D':        # l'adversaire a riposté au tour 2
        return hist_adv[-1]       # TIT-FOR-TAT
    cycle = ['C', 'C', 'D']
    return cycle[(tour - 1) % 3]


def joss(mon_hist, hist_adv, rng):
    """JOSS : TFT, mais remplace C par D avec 10 % de chances (y compris au tour 1)."""
    coup = tit_for_tat(mon_hist, hist_adv, rng)
    if coup == 'C' and rng.random() < 0.10:
        return 'D'
    return coup



# Population de base utilisée par les tournois
STRATEGIES_COURS = {
    "ALL-D": all_d,
    "RANDOM": random_strat,
    "TIT-FOR-TAT": tit_for_tat,
    "TESTER": tester,
    "JOSS": joss,
}
