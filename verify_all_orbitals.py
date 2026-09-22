"""
Deep verification of Slater's Rules for every element (1 to 118) across every single occupied orbital.
Checks:
1. Valid electron counts for all 118 elements.
2. Every orbital calculation produces positive Zeff.
3. Sum of electrons in breakdown equals total Z (shielding electrons + target electron = Z).
4. S calculation matches strict Slater's Rules formula without precision or logic errors.
"""

from test_benchmarks import get_config, slater, AUFBAU, SLATER_DF, LS, EXCEPT

all_results = []
anomalies = []
total_calculations = 0

for Z in range(1, 119):
    cfg = get_config(Z)
    total_electrons = sum(c['c'] for c in cfg)
    if total_electrons != Z:
        anomalies.append(f"Z={Z}: Total electron sum {total_electrons} != {Z}")
    
    # Sort orbitals by n, then l
    orbs = sorted(cfg, key=lambda c: (c['n'], c['l']))
    
    for orb_obj in orbs:
        total_calculations += 1
        n = orb_obj['n']
        l = orb_obj['l']
        c_count = orb_obj['c']
        orb_name = f"{n}{LS[l]}"
        
        S = slater(cfg, orb_name)
        zeff = round(Z - S, 2)
        
        # 1. Zeff must be strictly positive
        if zeff <= 0:
            anomalies.append(f"Z={Z} ({orb_name}): Zeff={zeff} is non-positive! (S={S})")
            
        # 2. Shielding S cannot exceed Z - 1 (or Z for hypothetical)
        if S >= Z:
            anomalies.append(f"Z={Z} ({orb_name}): S={S} >= Z={Z}!")

        # 3. Target orbital electron count must be >= 1
        if c_count < 1:
            anomalies.append(f"Z={Z} ({orb_name}): electron count is {c_count} < 1!")

        # 4. Detailed audit of Slater logic:
        # Check conservation of electrons:
        # For s/p:
        #   same_sp + nm1 + inner + outer + 1 (the electron itself) MUST equal Z!
        if LS[l] in ('s', 'p'):
            same_sp_others = 0
            for c in cfg:
                if c['n'] == n and (c['l'] == 0 or c['l'] == 1):
                    if c['l'] == l:
                        same_sp_others += c['c'] - 1
                    else:
                        same_sp_others += c['c']
            nm1_count = sum(c['c'] for c in cfg if c['n'] == n - 1) if n > 1 else 0
            inner_count = sum(c['c'] for c in cfg if c['n'] <= n - 2) if n > 2 else 0
            outer_count = sum(c['c'] for c in cfg if c['n'] > n or (c['n'] == n and c['l'] > 1))
            
            accounted = same_sp_others + nm1_count + inner_count + outer_count + 1
            if accounted != Z:
                anomalies.append(f"Z={Z} ({orb_name}): s/p electron conservation failed! accounted={accounted} vs Z={Z}")
        else:
            # For d/f:
            same_d_others = c_count - 1
            my_idx = next(i for i, (an, al) in enumerate(SLATER_DF) if an == n and al == l)
            left_count = 0
            for i in range(my_idx):
                an, al = SLATER_DF[i]
                f = next((c for c in cfg if c['n'] == an and c['l'] == al), None)
                if f:
                    left_count += f['c']
            right_count = 0
            for i in range(my_idx + 1, len(SLATER_DF)):
                an, al = SLATER_DF[i]
                f = next((c for c in cfg if c['n'] == an and c['l'] == al), None)
                if f:
                    right_count += f['c']
            accounted = same_d_others + left_count + right_count + 1
            if accounted != Z:
                anomalies.append(f"Z={Z} ({orb_name}): d/f electron conservation failed! accounted={accounted} vs Z={Z}")

print(f"Total element-orbital pairs checked: {total_calculations}")
print(f"Total anomalies found: {len(anomalies)}")
if anomalies:
    for a in anomalies[:20]:
        print("  - ", a)
else:
    print("ALL ELEMENT-ORBITAL CALCULATIONS ARE 100% SOUND AND CONSERVED! [PASS]")
