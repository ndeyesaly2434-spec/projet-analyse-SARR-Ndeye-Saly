import json
import os

import matplotlib.pyplot as plt
import pandas as pd

# Lecture du fichier
df = pd.read_csv("data/logs_reseau.csv")

# Nettoyage
df = df.drop_duplicates()
df["protocol"] = df["protocol"].str.upper()
df["bytes_sent"] = df["bytes_sent"].fillna(df["bytes_sent"].median())
df["timestamp"] = pd.to_datetime(df["timestamp"])


# Les 5 résultats
nb_lignes = len(df)
top_port = df["dst_port"].value_counts().idxmax()
taux_deny = round((df["action"] == "DENY").mean() * 100, 2)
ip_scanner = df.groupby("src_ip")["dst_port"].nunique().idxmax()
ip_exfiltration = df.groupby("src_ip")["bytes_sent"].sum().idxmax()

# Enregistrement dans resultats.json
resultats = {
    "nb_lignes_apres_nettoyage": int(nb_lignes),
    "top_port": int(top_port),
    "taux_deny_pct": float(taux_deny),
    "ip_scanner": str(ip_scanner),
    "ip_exfiltration": str(ip_exfiltration),
}

with open("resultats.json", "w") as f:
    json.dump(resultats, f, indent=2)

print(resultats)