# ACE-Receipt Spec: Draft V0

Standard minimal de preuve d'exécution agentique.

## Champs obligatoires (V0)

| Champ | Type | Description |
|---|---|---|
| receipt_id | string | UUID v4 |
| date_utc | ISO 8601 | Horodatage script, pas LLM |
| sources | string[] | URLs réellement lues par le script |
| model | string | Modèle appelé (ex: deepseek-chat) |
| content_hash | sha256 | Hash du contenu note générée |
| operator | string | Identifiant humain responsable |
| confidence | null \| int | Métrique calculée ou null: jamais auto-déclarée par le LLM |
| status | enum | DRAFT / REVIEWED / PUBLISHED |

## Principe fondateur

Le receipt est produit par le script d'orchestration.  
Jamais par le LLM. Le LLM ne s'audite pas lui-même.
