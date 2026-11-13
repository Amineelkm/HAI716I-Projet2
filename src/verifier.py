"""
Vérifications du moteur sur des cas dont on connaît le résultat à l'avance.
À lancer avant les vrais tournois : python src/verifier.py
"""

import random

from moteur import partie, tournoi
from strategies import all_d, tit_for_tat, tester, STRATEGIES_COURS


def all_c(mon_hist, hist_adv, rng):
    """Coopère toujours (sert seulement pour les tests)."""
    return 'C'


def verifier():
    """Lance chaque test et affiche OK, ou s'arrête avec une erreur."""
    rng = random.Random(0)

    sa, sb, _, _ = partie(all_d, all_d, 200, rng)
    assert (sa, sb) == (400, 400), (sa, sb)
    print("OK  ALL-D contre ALL-D : 400 / 400")

    sa, sb, _, _ = partie(tit_for_tat, tit_for_tat, 200, rng)
    assert (sa, sb) == (600, 600), (sa, sb)
    print("OK  TFT contre TFT : 600 / 600")

    sa, sb, _, _ = partie(tit_for_tat, all_d, 200, rng)
    assert (sa, sb) == (398, 403), (sa, sb)
    print("OK  TFT contre ALL-D : 398 / 403")

    sa, sb, _, _ = partie(all_c, all_d, 200, rng)
    assert (sa, sb) == (0, 1000), (sa, sb)
    print("OK  ALL-C contre ALL-D : 0 / 1000")

    _, _, h_tester, _ = partie(tester, all_c, 7, rng)
    assert h_tester == ['D', 'C', 'C', 'D', 'C', 'C', 'D'], h_tester
    print("OK  TESTER contre ALL-C : D, puis cycle C, C, D")

    _, _, h_tester, _ = partie(tester, all_d, 5, rng)
    assert h_tester == ['D', 'C', 'D', 'D', 'D'], h_tester
    print("OK  TESTER contre ALL-D : passe en TIT-FOR-TAT après la riposte")

    r1 = tournoi(STRATEGIES_COURS, graine=42)
    r2 = tournoi(STRATEGIES_COURS, graine=42)
    assert r1 == r2
    print("OK  même graine = mêmes résultats (reproductible)")

    print("\nToutes les vérifications sont passées.")


if __name__ == "__main__":
    verifier()
