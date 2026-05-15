# GAQL Cheatsheet da Skill

Este arquivo lista as queries usadas pela skill e explica o objetivo de cada bloco.

## Conversões

```sql
SELECT
  conversion_action.id,
  conversion_action.name,
  conversion_action.status,
  conversion_action.type,
  conversion_action.category,
  conversion_action.counting_type,
  conversion_action.primary_for_goal,
  conversion_action.attribution_model_settings.attribution_model,
  conversion_action.click_through_lookback_window_days,
  metrics.conversions,
  metrics.all_conversions
FROM conversion_action
WHERE conversion_action.status != 'REMOVED'
```

Usada para encontrar conversões ativas, primárias, categoria de venda, modelo de atribuição e volume.

## Tracking

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  metrics.clicks,
  metrics.conversions,
  metrics.all_conversions,
  metrics.view_through_conversions,
  segments.date
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

Usada para detectar campanhas com cliques sem conversão e diferença entre conversions e all_conversions.

## Estrutura

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.advertising_channel_type,
  campaign.advertising_channel_sub_type,
  campaign.bidding_strategy_type,
  campaign.network_settings.target_google_search,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign.network_settings.target_partner_search_network,
  campaign_budget.amount_micros,
  campaign.target_cpa.target_cpa_micros,
  campaign.target_roas.target_roas
FROM campaign
WHERE campaign.status = 'ENABLED'
```

Usada para ver canal, redes ativadas, estratégia de lance e metas.

## Remarketing

```sql
SELECT
  user_list.id,
  user_list.name,
  user_list.size_for_display,
  user_list.size_for_search,
  user_list.membership_status,
  user_list.membership_life_span
FROM user_list
WHERE user_list.membership_status = 'OPEN'
```

Mostra tamanho e janela das listas.

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.advertising_channel_type,
  ad_group_criterion.user_list.user_list
FROM ad_group_criterion
WHERE ad_group_criterion.type = 'USER_LIST'
  AND campaign.status = 'ENABLED'
```

Mostra campanhas com audiência associada.

## Keywords

```sql
SELECT
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.status,
  ad_group_criterion.quality_info.quality_score,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions
FROM keyword_view
WHERE ad_group_criterion.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

Mostra qualidade, gasto, cliques e conversões por palavra.

## Anúncios

```sql
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.type,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad.responsive_search_ad.descriptions,
  ad_group_ad.ad_strength,
  ad_group_ad.status,
  metrics.impressions,
  metrics.clicks,
  metrics.conversions
FROM ad_group_ad
WHERE ad_group_ad.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

Mostra força do anúncio, tipo e performance.

## Budget

```sql
SELECT
  campaign.id,
  campaign.name,
  campaign_budget.amount_micros,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_impression_share,
  metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED'
  AND segments.date DURING LAST_30_DAYS
```

Mostra perda por verba, rank e cobertura de impressão.
